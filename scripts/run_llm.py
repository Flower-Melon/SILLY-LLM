"""Generate SMART-LLM plans with DeepSeek V4.1 Flash for one benchmark level."""

import argparse
import copy
import json
from datetime import datetime
from pathlib import Path
import re
import sys

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from resources.actions import ai2thor_actions
from resources.robots import robots

API_KEY_FILE = ROOT / "key.txt"
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-flash"
MAX_TOKENS = 8192

CODE_INSTRUCTIONS = (
    "Return only Python source code; put explanations in Python comments. "
    "Do not use Markdown fences or import the skills module. "
    "Use only the listed skill functions, which are provided by the executor. "
    "Join all task threads before finishing."
)
ALLOCATION_INSTRUCTIONS = (
    "You are a Robot Task Allocation Expert. Allocate subtasks to the minimum "
    "number of robots needed. Respect each robot's skills and mass_capacity. "
    "Form teams when one robot cannot satisfy the skill or mass requirements. "
    "Use sequential execution for dependencies and shared robots; use parallel "
    "execution for independent subtasks with available robots. Explain the allocation."
)


def create_session():
    key = API_KEY_FILE.read_text(encoding="utf-8-sig").strip()
    if not key:
        raise RuntimeError("Fill the project's root key.txt with your DeepSeek API key.")
    session = requests.Session()
    # DeepSeek is reached directly; do not inherit Windows/system proxy settings.
    session.trust_env = False
    session.headers.update({"Authorization": f"Bearer {key}"})
    return session


def ask_deepseek(session, messages, max_tokens=MAX_TOKENS):
    response = session.post(API_URL, json={
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": False,
        "thinking": {"type": "disabled"},
    }, timeout=(15, 180))
    response.raise_for_status()
    choice = response.json()["choices"][0]
    if choice["finish_reason"] == "length":
        raise RuntimeError("DeepSeek output was truncated; increase MAX_TOKENS in run_llm.py.")
    text = (choice["message"]["content"] or "").strip()
    if not text:
        raise RuntimeError("DeepSeek returned an empty answer.")
    return text


def extract_python_code(text):
    blocks = re.findall(r"```(?:python|py)?[ \t]*\r?\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return "\n\n".join(block.strip() for block in blocks) if blocks else text.strip()


def get_ai2_thor_objects(floor_plan):
    from ai2thor.controller import Controller

    controller = Controller(scene=f"FloorPlan{floor_plan}")
    try:
        return [{"name": obj["objectType"], "mass": obj["mass"]}
                for obj in controller.last_event.metadata["objects"]]
    finally:
        controller.stop()


def task_robots(robot_ids):
    available = [copy.deepcopy(robots[robot_id - 1]) for robot_id in robot_ids]
    for index, robot in enumerate(available, 1):
        robot["name"] = f"robot{index}"
    return available


def generate_plan(session, task, available, objects, examples):
    skills = f"# Available skill functions:\n{ai2thor_actions}\nimport time\nimport threading"
    world = f"\n\nobjects = {objects}"
    description = f"\n\n# Task Description: {task}"
    decomposition = ask_deepseek(session, [
        {"role": "system", "content": CODE_INSTRUCTIONS},
        {"role": "user", "content": skills + world + "\n\n" + examples["decompose"] + description},
    ])
    decomposition = extract_python_code(decomposition)

    allocation_prompt = (
        skills + "\n\n" + examples["allocation"] + description + "\n" + decomposition
        + f"\n\n# TASK ALLOCATION\nrobots = {available}" + world
        + "\n# SOLUTION\n"
    )
    allocation = ask_deepseek(session, [
        {"role": "system", "content": ALLOCATION_INSTRUCTIONS},
        {"role": "user", "content": allocation_prompt},
    ])

    code_prompt = (
        skills + world + "\n\n" + examples["code"] + description + "\n" + decomposition
        + f"\n\n# TASK ALLOCATION\nrobots = {available}\n" + allocation
        + "\n# CODE Solution\n"
    )
    code = ask_deepseek(session, [
        {"role": "system", "content": "You are a Robot Task Allocation Expert. " + CODE_INSTRUCTIONS},
        {"role": "user", "content": code_prompt},
    ])
    return decomposition, allocation, extract_python_code(code)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", choices=["elemental", "simple", "compound", "complex"],
                        help="Benchmark level under data/final_test (required unless --check-api).")
    parser.add_argument("--check-api", action="store_true", help="Check DeepSeek without starting AI2-THOR.")
    args = parser.parse_args(argv)

    if not args.check_api and not args.level:
        parser.error("--level is required unless --check-api is used.")

    with create_session() as session:
        print(f"DeepSeek model: {MODEL}")
        if args.check_api:
            answer = ask_deepseek(session, [{"role": "user", "content": "Reply with exactly OK."}],
                                  max_tokens=128)
            print(f"API check succeeded: {answer}")
            return

        tasks = json.loads((ROOT / "data/final_test" / f"{args.level}.json")
                           .read_text(encoding="utf-8"))
        objects_cache = {}
        prompt_dir = ROOT / "data/pythonic_plans"
        examples = {
            "decompose": (prompt_dir / "train_task_decompose.py").read_text(encoding="utf-8"),
            "allocation": (prompt_dir / "train_task_allocation_solution.py").read_text(encoding="utf-8"),
            "code": (prompt_dir / "train_task_allocation_code.py").read_text(encoding="utf-8"),
        }
        stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        for index, task in enumerate(tasks, 1):
            print(f"[{index}/{len(tasks)}] FloorPlan{task['floor_plan']}: {task['task']}")
            objects = objects_cache.get(task["floor_plan"])
            if objects is None:
                objects = get_ai2_thor_objects(task["floor_plan"])
                objects_cache[task["floor_plan"]] = objects
            available = task_robots(task["robot list"])
            decomposition, allocation, code = generate_plan(session, task["task"], available, objects, examples)
            task_name = re.sub(r"[^\w-]+", "_", task["task"]).strip("_")
            folder = ROOT / "logs" / args.level / f"{task_name}_plans_{stamp}"
            folder.mkdir(parents=True)
            (folder / "decomposed_plan.py").write_text(decomposition + "\n", encoding="utf-8")
            (folder / "allocated_plan.txt").write_text(allocation + "\n", encoding="utf-8")
            (folder / "code_plan.py").write_text(code + "\n", encoding="utf-8")
            metadata = {"task": task["task"], "model": MODEL, "level": args.level,
                        "floor_plan": task["floor_plan"], "objects": objects, "robots": available,
                        "ground_truth": task["object_states"],
                        "trans": task["trans"], "max_trans": task["max_trans"]}
            (folder / "task.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
            print(f"Saved: {folder}")


if __name__ == "__main__":
    main()
