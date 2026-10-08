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
python scripts/run_llm.py --floor-plan 6
```

`--check-api` 发送一次简短请求，会消耗少量 API 额度，不启动 Unity。
`--floor-plan` 默认是 6；其他可用场景为 15、21、201、209、303、414。
首次启动 AI2-THOR 会下载场景构建，需要网络连接。

生成计划后，查看 `logs` 中的目录和 `code_plan.py`，再执行：

```bash
python scripts/execute_plan.py --command 生成目录的名称
```

`--command` 只填写 `logs/` 下的目录名。
旧版依赖 `log.txt` 的日志请重新生成。

## 简化后的架构

```text
key.txt + 场景任务 JSON + 机器人能力 + AI2-THOR 场景物体
    ↓
scripts/run_llm.py
    ├── DeepSeek：任务分解
    ├── DeepSeek：联盟形成与任务分配推理
    └── DeepSeek：机器人执行代码
    ↓
logs/<任务目录>/
    ├── decomposed_plan.py
    ├── allocated_plan.txt
    ├── code_plan.py
    └── task.json
    ↓
scripts/execute_plan.py + data/aithor_connect/ 模板
    ↓
executable_plan.py → AI2-THOR 执行、评估、图像与视频
```

| 路径 | 作用 |
| --- | --- |
| `scripts/run_llm.py` | 读取任务、构造提示词、调用 DeepSeek、保存每条任务的结果 |
| `scripts/execute_plan.py` | 从 `task.json` 读取配置并拼接、运行执行脚本 |
| `data/final_test/` | 7 个场景，36 条任务，文件均为标准 JSON 数组 |
| `data/pythonic_plans/` | 原始 few-shot 示例，只作为文本提示读取，不是训练脚本 |
| `data/aithor_connect/` | 动作队列、仿真函数、目标状态评估和视频输出 |
| `resources/robots.py` | 28 种机器人配置，载重字段统一为 `mass_capacity` |
| `resources/actions.py` | 提示词允许使用的已实现动作 |
| `scripts/ai2_thor_controller.py` | 原仓库的独立演示，不参与正式规划与执行流程 |
| `tests/test_reproduction.py` | 数据、HTTP 调用、规划与执行脚本、评估的离线测试 |

规划脚本只保留 `--floor-plan`、`--check-api`；执行脚本只保留 `--command`。
模型、地址、密钥文件路径固定在代码中。关闭思考，温度为 0，规划输出预算为 8192 tokens。
每条任务依次请求三个阶段并立即保存，单个场景会处理文件中的全部任务。
DeepSeek 使用 HTTPS 直连，保留证书校验，不继承系统代理；这样避开此前 Windows 代理的 TLS 错误。

## 数据修复说明

保留全部 36 条任务及原有机器人组合，修复了以下问题：

- 所有文件从逐行记录改为标准 JSON 数组；加载器直接使用 `json.loads()`。
- Python `None` 和字符串 `"None"` 改为 JSON `null`。
- FloorPlan303 中缺失的两个 `object_states` 数组闭合括号已补齐。
- FloorPlan209 的“Turn off floor lamp”补充了 `FloorLamp/OFF` 目标和两个计数字段。
- FloorPlan21 的“Slice apple and throw it in the trash”补充了两个计数字段。
- 两条任务缺失的 `trans`、`max_trans` 均按 0 补填；这是修复时推定的默认值，不是恢复出的作者标签。
- 清理 `CoffeeTable,`、`CellPhone `、`GarbageCan ` 的多余标点和空格。
- 浴室标签中的 `trash`、`cloth`、`cabinet` 统一为 `GarbageCan`、`Cloth`、`Cabinet`。
- “Put plunger in cabinet”补充了柜子中应包含 `Plunger` 的目标。

原数据仍有一些不完整的语义标签。例如 FloorPlan414 第一条“Fill water in the BathTub”
原本没有目标标签，未凭空补造仿真结果；执行器会提示无法评估，且不会将它自动算作成功。
其他原有目标未扩写，语法和字段修复不代表已经逐项验证全部场景物体与任务语义。

评估器补充 `BROKEN` 检查，同一目标只计一次；容器中的多个要求必须同时满足，
避免重复物体或多个容纳物使 GCR 超过 1。保留原资源利用率 RU 的代码段估算，
它不是实时机器人利用率。这里的复现目标是跑通框架，不保证恢复论文的相同指标。

## 验证

```bash
python -m unittest discover -s tests -v
```

离线测试不调用真实 API，也不启动 Unity。完整仿真仍需在 Ubuntu 上运行上述生成与执行命令。