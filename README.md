# 小卡健康 Agent

小卡是一个用 AI 帮你记录和整理健康信息的个人健康助手。它可以记录饮食、体重、运动、睡眠、补剂和体检资料，并把这些记录整理成每日数据、周报和月报。

这个仓库保存的是小卡的说明、规则、模板、知识库和示例数据。真实的个人健康数据默认保存在你自己的电脑里，不会提交到仓库。

## 当前状态

小卡现在处于“可试用，但仍在完善”的阶段。

已经完成并验证的部分：

- 可以引导创建个人健康档案和目标。
- 可以记录饮食、体重、体检、运动、补剂、睡眠和目标调整。
- 可以使用本地文件保存每日记录、整理后的每日数据、体检资料、报告和个人食物库。
- 已经配置自动整理任务：每天整理前一天记录，每天检查记录是否一致，每周生成周报，每月生成月报。
- 周报和月报已经通过“没有数据”和“示例数据”两类测试：没有数据时会保持安静，不会发送无意义提醒。
- 已经定义 Apple Watch / Apple Health 的单张运动、活动、睡眠截图记录方式，并用示例数据验证了从“确认后的识别结果”到每日数据的整理流程。
- 已经定义跨维度观察，例如把饮食、体重、运动、活动和睡眠放在一起看；数据不足时会明确说数据不足，不会硬编结论。
- 已经补充药物、运动、睡眠深度分析的报告模板和示例数据。
- 已经补充公开发布前检查清单、隐私边界、医学边界和 AI 能力要求。

仍在等待真实使用验证的部分：

- 真实 Apple Watch / Apple Health 截图识别还没有完成集中测试。
- 跨维度观察还没有完成真实自动周报/月报测试。
- 药物、运动、睡眠深度分析还没有完成真实自动报告测试。
- Apple Health 历史批量导入、Health Auto Export、体脂秤导入、Telegram 快捷操作和静态数据看板暂未实现。

## 小卡能做什么

| 能力 | 当前说明 |
|------|----------|
| 健康档案 | 通过问答收集身高、体重、目标、活动水平、运动背景、用药和补剂背景 |
| 饮食记录 | 记录文字描述、食物照片或菜单截图中的饮食信息，估算热量和营养素 |
| 体重追踪 | 保存体重记录，观察近期变化和目标差距 |
| 运动记录 | 记录手动运动描述，也支持整理单张 Apple Watch / Apple Health 运动截图中的关键信息 |
| 活动记录 | 记录步数、活动消耗等日级活动摘要 |
| 睡眠记录 | 记录睡眠时长、睡眠窗口和睡眠质量，也支持整理单张睡眠截图中的关键信息 |
| 补剂管理 | 记录补剂和剂量，提醒可能需要注意的药物或补剂边界 |
| 体检解读 | 整理体检指标，标记需要关注的异常项，但不替代医生诊断 |
| 周报和月报 | 自动汇总一周或一个月的记录，写入报告文件 |
| 跨维度观察 | 在数据足够时，低强度观察饮食、体重、运动、活动和睡眠之间的关系 |
| 目标更新 | 调整体重、热量、蛋白质等目标 |
| 健康问答 | 根据仓库里的营养、医学、运动、补剂和设备知识库回答问题 |

## 它不做什么

- 不提供医疗诊断。
- 不开处方，不建议自行调整处方药剂量。
- 不在数据不足时强行给出趋势或因果结论。
- 不做实时运动追踪。
- 不做食品条码扫描。
- 当前不做 Apple Health 历史数据批量导入。
- 当前不做体脂秤或其他外部设备自动导入。
- 当前不自带远端数据库或账号系统。

## 数据如何保存

小卡使用本地文件保存数据。默认路径如下：

| 内容 | 保存位置 |
|------|----------|
| 个人档案和目标 | `config/` |
| 每天的文字记录 | `workspace/logs/` |
| 每天整理后的数据 | `workspace/data/` |
| 体检资料 | `workspace/medical/` |
| 周报和月报 | `workspace/reports/` |
| 个人食物库 | `workspace/food-library/` |

`config/` 和 `workspace/` 中的个人文件默认不会提交到 GitHub。仓库里只保留模板、说明和非个人示例数据。

## 隐私和医学边界

- 健康记录默认保存在本地电脑。
- 如果你使用云端 AI 服务，发送给 AI 的文字、截图、图片和必要上下文可能会被服务提供商处理。
- 如果你想尽量减少外部传输，可以改用本地 AI；但如果要处理截图或照片，本地 AI 也必须能识别图片。
- 小卡的输出只能作为记录整理和健康管理参考，不构成诊断、治疗方案或处方建议。

更多边界说明见 [隐私与医学边界](docs/privacy-and-medical-boundaries.md)。

## 对 AI 能力的要求

小卡不绑定某一个固定 AI。不同使用环境可以选择不同 AI。

基本要求：

- 能稳定理解中文健康记录。
- 能按要求读写本地文件。
- 能遵守“数据不足就不下结论”的规则。
- 如果要处理食物照片、运动截图、睡眠截图、营养标签或体检单图片，AI 必须能理解图片或识别图片里的文字。

如果 AI 不能稳定识别图片，用户需要手动把截图里的关键字段转成文字，例如日期、来源、运动类型、时长、活动消耗、睡眠时长等。

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/MochenRay/xiaoka-health-agent.git
cd xiaoka-health-agent
```

### 2. 准备本地数据目录

```bash
mkdir -p workspace/{logs,data,medical,reports,food-library}
printf '[]\n' > workspace/food-library/my-foods.json
```

### 3. 在你的 AI 工具中打开这个仓库

可以使用 OpenClaw、Claude Code 或其他能读取本地仓库的 AI 工具。第一次对话时，小卡会先引导你创建个人健康档案。

示例：

```text
你：你好
小卡：你好，我是小卡。你还没有配置健康档案，我先帮你完成初始化。
```

## 示例使用方式

```text
你：午饭吃了一碗牛肉面加一个煎蛋
小卡：已记录午餐，并估算本餐热量、蛋白质、碳水和脂肪。
```

```text
你：今天体重 101.2kg
小卡：已记录今天体重，并会在后续报告里用于观察趋势。
```

```text
你：这是今天 Apple Watch 的运动截图
小卡：我会先识别日期、运动类型、时长、活动消耗和来源；如果识别不确定，会先向你确认。
```

## 仓库内容

| 路径 | 说明 |
|------|------|
| `README.md` | GitHub 首页说明 |
| `agent.md` / `SOUL.md` | 小卡的人设和行为规则 |
| `SKILL.md` | 小卡可处理的任务路线 |
| `config/` | 个人档案和目标模板 |
| `templates/` | 每日日志、周报、月报模板 |
| `references/` | 营养、医学、药物、补剂、运动和设备知识库 |
| `docs/` | 更详细的说明、数据格式、运行方式和边界 |
| `fixtures/` | 不含个人健康数据的示例数据 |
| `scripts/` | 用来检查示例数据和文档是否一致的工具 |
| `workspace/` | 真实使用时的本地数据目录 |
| `deploy/` | 部署说明 |
| `plans/` | 路线图和后续计划 |

## 给维护者的检查

仓库里包含非个人示例数据，用来检查说明、模板和示例是否一致。

常用检查命令：

```bash
python3 scripts/validate_repository_contract.py
python3 scripts/validate_settlement_prompt_contract.py
python3 scripts/validate_daily_json_schema.py
python3 scripts/validate_report_contracts.py
python3 scripts/validate_phase2b_fixtures.py
python3 scripts/validate_phase2c_screenshot_fixtures.py
python3 scripts/validate_phase3a_c8_fixtures.py
```

这些检查只能证明示例数据和仓库说明一致，不能证明真实截图识别、真实自动报告或个人健康数据已经完全闭环。

## 更多文档

- [最小使用约定](docs/phase1-minimum-contract.md)
- [数据保存格式](docs/data-schema.md)
- [自动报告说明](docs/report-automation.md)
- [OpenClaw 部署说明](deploy/openclaw-setup.md)
- [Claude Code 部署说明](deploy/claude-code-setup.md)
- [公开发布检查清单](docs/public-release-checklist.md)
- [知识库来源](docs/knowledge-base-sources.md)

## 贡献

欢迎提交改进：

- 修正食物营养数据。
- 补充体检指标说明。
- 改进日志或报告模板。
- 补充不含个人信息的示例数据。
- 改进文档中不清楚或容易误解的地方。

## 致谢

- [health-coach](https://github.com/MochenRay/health-coach)：本项目的早期来源。
- [china-food-composition-data](https://github.com/Sanotsu/china-food-composition-data)：中国食物成分表 JSON 数据来源之一。

## License

MIT
