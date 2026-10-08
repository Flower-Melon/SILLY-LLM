"""Assemble and execute a generated plan in AI2-THOR."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def append_trans_ctr(code):
    return sum(1 for block in code.split("\n\n")
               if block.strip().endswith(")")
               and not any(word in block for word in ("def ", "threading.Thread", "join")))


def compile_aithor_exec_file(command):
    folder = ROOT / "logs" / command
    metadata = json.loads((folder / "task.json").read_text(encoding="utf-8"))
    templates = ROOT / "data/aithor_connect"
    code = (folder / "code_plan.py").read_text(encoding="utf-8")
    parts = [
        (templates / "imports_aux_fn.py").read_text(encoding="utf-8"),
        f"robots = {metadata['robots']!r}\nfloor_no = {metadata['floor_plan']!r}\n"
        f"ground_truth = {metadata['ground_truth']!r}\n"
        f"no_trans_gt = {metadata['trans']!r}\nmax_trans = {metadata['max_trans']!r}\n",
        (templates / "aithor_connect.py").read_text(encoding="utf-8"),
        code,
        f"no_trans = {append_trans_ctr(code)}",
        (templates / "end_thread.py").read_text(encoding="utf-8"),
    ]
    executable = folder / "executable_plan.py"
    executable.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return str(executable)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True, help="Generated folder name under logs/.")
    args = parser.parse_args()
    executable = compile_aithor_exec_file(args.command)
    subprocess.run([sys.executable, executable], check=True)


if __name__ == "__main__":
    main()
