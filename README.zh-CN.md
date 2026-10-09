# SMART-LLM：使用 DeepSeek 复现多机器人任务规划

[项目主页](https://sites.google.com/view/smart-llm/) | [论文](https://arxiv.org/abs/2309.10062)

项目保留原框架的三个阶段：任务分解、联盟形成与任务分配推理、执行代码生成。
现在固定使用 DeepSeek V4.1 Flash，直接通过 HTTP 调用 `deepseek-flash`。
根目录 `key.txt` 是唯一的密钥入口；不需要 OpenAI SDK、环境变量或密钥文件参数。

## Ubuntu 下运行

使用有桌面显示和 OpenGL/GLX 的 Ubuntu 环境。AI2-THOR 会启动 Unity，执行器会显示 OpenCV 窗口。
Windows 中现有的 conda 环境不能直接作为 Ubuntu 环境使用，需要在 Ubuntu 中创建环境。
如果已经有 Linux 的 `smartllm` 环境，直接激活并安装依赖即可。

```bash
conda create -n smartllm python=3.10 -y
conda activate smartllm
python -m pip install -r requirments.txt
sudo apt-get install ffmpeg libgl1 libglib2.0-0
```

将 DeepSeek API Key 写入项目根目录的 `key.txt`，文件中只放密钥，使用 UTF-8 编码。
迁移项目时请同时带上这个文件；它被 Git 忽略，不会随提交迁移。

在项目根目录先检查 API，再生成计划：

```bash
python scripts/run_llm.py --check-api
python scripts/run_llm.py --level simple
```

`--check-api` 发送一次简短请求，会消耗少量 API 额度，不启动 Unity。
`--level` 取 elemental / simple / compound / complex，对应 `data/final_test/` 下的四个难度文件；
每条任务自带 `floor_plan`，脚本按需启动对应场景获取物体列表。
首次启动 AI2-THOR 会下载场景构建，需要网络连接。

生成计划后，计划按难度保存在 `logs/<难度>/` 下；查看任务目录和 `code_plan.py`，再执行：

```bash
python scripts/execute_plan.py --command simple                 # 整个难度：依次执行全部任务并输出平均指标
python scripts/execute_plan.py --command simple/<任务目录名>     # 单条任务（原有功能）
```

`--command` 填 `logs/` 下的路径：难度目录（如 `simple`）会逐个执行该难度下的所有任务，
并在结尾汇总 SR/TC/GCR/Exec/RU 平均值，写入 `logs/<难度>/evaluation_summary_<时间戳>.txt`；
执行失败的任务按全 0 计入平均值并在汇总中列出。旧版一级目录（如 `logs/Slice_the_tomato_plans_...`）仍可直接传入执行单条任务。
单次执行超过 `--timeout` 秒（默认 600，可传 0 关闭）会被连同 AI2-THOR 进程一起终止并自动重跑（`--retries`，默认 3 次）；
机器人出生位置每次随机，因此重跑可以摆脱"闲置机器人挡路导致卡死"的问题。
执行时不再写 `img_*.png` 帧图，只保存每个视角的 `video_*.mp4` 视频（连续相同的静止画面会被去重跳过，视频时长会短于真实运行时长）；评估结果在视频收尾前就写入 `evaluation.txt`，超时中断也不会丢结果；
终端输出完整记录在 `run_log.txt`，单条任务的最终评估结果（SR/TC/GCR/Exec/RU）写入 `evaluation.txt`。
旧版依赖 `log.txt` 的日志请重新生成。
机器人出生点会保持至少 1 米间距，减少开局互相挡路；导航连续多次无进展（疑似被其他机器人的碰撞体积挡住）时，
执行器先把长期静止在附近或目标旁的闲置机器人挪开，没有可挪的阻挡者时再把执行机器人传送到候选目标点脱困，不再无限等待。

## 简化后的架构

```text
key.txt + 场景任务 JSON + 机器人能力 + AI2-THOR 场景物体
    ↓
scripts/run_llm.py
    ├── DeepSeek：任务分解
    ├── DeepSeek：联盟形成与任务分配推理
    └── DeepSeek：机器人执行代码
    ↓
logs/<难度>/<任务目录>/
    ├── decomposed_plan.py
    ├── allocated_plan.txt
    ├── code_plan.py
    └── task.json
    ↓
scripts/execute_plan.py + data/aithor_connect/ 模板
    ↓
executable_plan.py → AI2-THOR 执行、评估、视频录制与结果文件
```

## 验证

```bash
python -m unittest discover -s tests -v
```

离线测试不调用真实 API，也不启动 Unity。完整仿真仍需在 Ubuntu 上运行上述生成与执行命令。