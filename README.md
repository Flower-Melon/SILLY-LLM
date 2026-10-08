# **SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models**

Shyam Sundar Kannan, Vishnunandan L. N. Venkatesh, and Byung-Cheol Min. 

Submitted to IEEE International Conference on Robotics and Automation (ICRA ), 2024

[Project Page](https://sites.google.com/view/smart-llm/) | [arXiv](https://arxiv.org/abs/2309.10062) | [Video](https://www.youtube.com/watch?v=mssTPl7ifyI)

**Abstract:** In this work, we introduce SMART-LLM, an innovative framework designed for embodied multi-robot task planning. SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models (LLMs), harnesses the power of LLMs to convert high-level task instructions provided as input into a multi-robot task plan. It accomplishes this by executing a series of stages, including task decomposition, coalition formation, and task allocation, all guided by programmatic LLM prompts within the few-shot prompting paradigm. We create a benchmark dataset designed for validating the multi-robot task planning problem, encompassing four distinct categories of high-level instructions that vary in task complexity. Our evaluation experiments span both simulation and real-world scenarios, demonstrating that the proposed model can achieve promising results for generating multi-robot task plans.

## Reproduction with DeepSeek

See [the Chinese guide](README.zh-CN.md) for the architecture and Ubuntu setup.
The planner uses DeepSeek V4.1 Flash directly over HTTP. The model is fixed to
`deepseek-flash`; put your DeepSeek API key in the root `key.txt` (ignored by Git).
There is no OpenAI SDK dependency or provider/configuration switching.

Use Ubuntu with a working graphical session and OpenGL/GLX for AI2-THOR and OpenCV.
The Windows conda environment cannot be reused as a Linux environment.

```bash
conda create -n smartllm python=3.10 -y
conda activate smartllm
python -m pip install -r requirments.txt
sudo apt-get install ffmpeg libgl1 libglib2.0-0
```

From the repository root:

```bash
python scripts/run_llm.py --check-api
python scripts/run_llm.py --floor-plan 6
python scripts/execute_plan.py --command <generated-folder-name>
```

The first command sends one short API request without starting Unity. The planner
only accepts `--floor-plan` (default: 6) and `--check-api`. Each task uses three
requests: decomposition, allocation reasoning, and executable code generation.
Thinking is disabled, temperature is 0, and the output budget is 8192 tokens.
DeepSeek connects directly without inheriting system proxy settings.

## Project layout

| Path | Purpose |
| --- | --- |
| `scripts/run_llm.py` | Load a scene's tasks and generate plans with DeepSeek |
| `scripts/execute_plan.py` | Read task metadata, assemble the script, run AI2-THOR |
| `data/final_test/` | Seven standard JSON arrays containing 36 tasks |
| `data/pythonic_plans/` | Original few-shot prompt examples, read as text |
| `data/aithor_connect/` | Simulator actions, evaluation, and video templates |
| `resources/` | Robot capabilities and supported action names |
| `tests/` | Offline data, API, planning, execution, and evaluation checks |
| `key.txt` | Your local DeepSeek key |
| `logs/` | Generated plans and task metadata |

Each generated folder contains `decomposed_plan.py`, `allocated_plan.txt`,
`code_plan.py`, and `task.json`. The executor adds `executable_plan.py`, images,
and videos. Earlier logs using `log.txt` should be regenerated.

The dataset now uses standard JSON arrays instead of JSONL. Malformed `None`
values, missing brackets, incomplete records, and obvious object-name typos were
repaired. Missing transition counts were filled with 0 and are inferred defaults,
not recovered author annotations. Original incomplete semantic labels are retained;
notably the first FloorPlan414 task has no goal labels and is reported as unevaluable
rather than automatically successful. The resource-use metric retains the original
sequential-block heuristic. These changes support running the framework, not exact
recovery of the paper's reported numbers.

```bash
python -m unittest discover -s tests -v
```

## Citation
If you find this work useful for your research, please consider citing:
```
@article{kannan2023smart,
    title={SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models},
  	author={Kannan, Shyam Sundar and Venkatesh, Vishnunandan LN and Min, Byung-Cheol},
  	journal={arXiv preprint arXiv:2309.10062},
 	year={2023}
}
```
