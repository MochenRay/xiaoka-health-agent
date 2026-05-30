# 小卡健康 Agent

小卡是一个本地文件驱动的 AI 健康助手。它帮助你记录饮食、体重、运动、睡眠、补剂和体检资料，并把这些记录整理成每日数据、周报和月报。

这个仓库保存的是 Agent 规则、模板、知识库、说明和非个人示例数据。真实健康数据默认保存在你自己的电脑里，不会提交到 GitHub。

## 当前状态

小卡现在处于“可试用，但仍在完善”的阶段。

已经可用：

- 引导创建个人健康档案和目标。
- 记录饮食、体重、体检、运动、补剂、睡眠和目标调整。
- 使用本地文件保存每日记录、每日 JSON、体检资料、报告和个人食物库。
- 通过 OpenClaw 定时任务整理前一天记录、校验结算、生成前日汇总、周报和月报。
- 周报和月报已验证“无数据静默”和“synthetic 示例数据生成报告”两类场景。
- Google Health API 已人工验证可读取来自 iOS Apple Health / HealthKit 的步数、睡眠和运动数据。
- Apple Watch / Apple Health 截图保留为 fallback；仓库用 synthetic fixtures 验证确认后的识别结果如何进入每日数据。
- 跨维度观察已定义：数据足够时低强度观察饮食、体重、运动、活动和睡眠之间的关系；数据不足时明确拒绝趋势或因果结论。
- 药物、运动、睡眠深度分析已有报告合同和 synthetic 示例。

## 小卡能做什么

| 能力 | 当前说明 |
|------|----------|
| 健康档案 | 通过问答收集身高、体重、目标、活动水平、运动背景、用药和补剂背景 |
| 饮食记录 | 记录文字描述、食物照片或菜单截图中的饮食信息，估算热量和营养素 |
| 体重追踪 | 保存体重记录，观察近期变化和目标差距 |
| 运动记录 | 记录手动运动描述；设备数据主路径改为 Google Health API，截图仅作为 fallback |
| 活动记录 | 记录步数、活动消耗等日级活动摘要 |
| 睡眠记录 | 记录睡眠时长、睡眠窗口和睡眠质量 |
| 补剂管理 | 记录补剂和剂量，提醒可能需要注意的药物或补剂边界 |
| 体检解读 | 整理体检指标，标记需要关注的异常项，但不替代医生诊断 |
| 周报和月报 | 自动汇总一周或一个月的记录，写入报告文件 |
| 跨维度观察 | 在数据足够时观察饮食、体重、运动、活动和睡眠之间的可能关系 |
| 目标更新 | 调整体重、热量、蛋白质等目标 |
| 健康问答 | 根据仓库里的营养、医学、运动、补剂和设备知识库回答问题 |

## 它不做什么

- 不提供医疗诊断。
- 不开处方，不建议自行调整处方药剂量。
- 不在数据不足时强行给出趋势、因果或跨维度结论。
- 不做实时运动追踪。
- 不做食品条码扫描。
- 当前还没有把 Google Health API 接入为正式自动同步器。
- 当前不做 Apple Health XML、Health Auto Export 或其他文件式批量导入。
- 当前不做体脂秤或其他外部设备自动导入。
- 当前不自带远端数据库或账号系统。

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

### 3. 在 AI 工具中打开仓库

可以使用 OpenClaw、Claude Code 或其他能读取本地仓库的 AI 工具。第一次对话时，小卡会先引导你创建个人健康档案。

```text
你：你好
小卡：你好，我是小卡。你还没有配置健康档案，我先帮你完成初始化。
```

示例：

```text
你：午饭吃了一碗牛肉面加一个煎蛋
小卡：已记录午餐，并估算本餐热量、蛋白质、碳水和脂肪。
```

```text
你：今天体重 101.2kg
小卡：已记录今天体重，并会在后续报告里用于观察趋势。
```

```text
你：同步最近两周的步数、睡眠和运动
小卡：我会优先走 Google Health API；如果没有授权或接口不可用，再用手动记录或截图 fallback。
```

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

`config/profile.md`、`config/goals.md` 和 `workspace/` 中的个人文件默认不会提交到 GitHub。仓库里的 `fixtures/synthetic/` 是维护者验证用的非个人示例数据，新用户可以忽略。

## 仓库内容

| 路径 | 说明 |
|------|------|
| `README.md` | GitHub 首页说明 |
| `agent.md` / `SOUL.md` | 小卡的人设和行为规则 |
| `SKILL.md` | 小卡可处理的任务路线 |
| `config/` | 个人档案和目标模板 |
| `templates/` | 每日日志、周报、月报模板 |
| `references/` | 营养、医学、药物、补剂、运动和设备知识库 |
| `docs/` | 数据格式、运行方式、边界和部署说明 |
| `fixtures/` | 维护者验证用的 synthetic 示例数据 |
| `scripts/` | 检查示例数据和文档合同的工具 |
| `workspace/` | 真实使用时的本地数据目录 |

## 边界和要求

- 健康记录默认保存在本地电脑。
- 如果使用云端 AI 服务，发送给 AI 的文字、截图、图片和必要上下文可能会被服务提供商处理。
- 如果启用 Google Health API，同步请求会经过 Google OAuth 和 Google Health API；token 和原始响应不得提交到 GitHub。
- 小卡输出只能作为记录整理和健康管理参考，不构成诊断、治疗方案或处方建议。
- 小卡不绑定固定 AI；如果要处理食物照片、营养标签、体检单或截图 fallback，所用模型必须能理解图片或识别图片文字。

更多边界说明见 [隐私与医学边界](docs/privacy-and-medical-boundaries.md)。

## 维护者验证

仓库内的 synthetic fixtures 用于检查说明、模板和示例是否一致，不能证明真实个人数据、真实截图识别或 Google Health API 自动同步已完整闭环。

```bash
python3 scripts/validate_repository_contract.py
python3 scripts/validate_google_health_importer.py
python3 scripts/validate_runtime_smoke_plan.py
python3 scripts/validate_settlement_prompt_contract.py
python3 scripts/validate_daily_json_schema.py
python3 scripts/validate_report_contracts.py
python3 scripts/validate_phase2b_fixtures.py
python3 scripts/validate_phase2c_screenshot_fixtures.py
python3 scripts/validate_phase3a_c8_fixtures.py
```

## 更多文档

- [最小使用约定](docs/phase1-minimum-contract.md)
- [数据保存格式](docs/data-schema.md)
- [Google Health API 接入决策](docs/google-health-api-ingestion.md)
- [自动报告说明](docs/report-automation.md)
- [OpenClaw 部署说明](docs/openclaw-setup.md)
- [知识库来源](docs/knowledge-base-sources.md)

## 贡献

欢迎提交改进：

- 修正食物营养数据。
- 补充体检指标说明。
- 改进日志或报告模板。
- 补充不含个人信息的 synthetic 示例数据。
- 改进文档中不清楚或容易误解的地方。

## 致谢

- [health-coach](https://github.com/MochenRay/health-coach)：本项目的早期来源。
- [china-food-composition-data](https://github.com/Sanotsu/china-food-composition-data)：中国食物成分表 JSON 数据来源之一。

## License

MIT
