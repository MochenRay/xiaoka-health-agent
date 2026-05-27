# 小卡健康 Agent

小卡是一个本地文件驱动的 AI 健康教练。它把健康档案、饮食、体重、运动、睡眠、补剂和体检记录放在本地 `config/` 与 `workspace/` 目录里，用 AI 帮你记录、整理、分析和生成报告。

## 当前状态

- Agent 核心工作流已可用：初始化、饮食、体重、体检、运动、补剂、睡眠、自建食物库、目标更新。
- OpenClaw 自动化已启用：零点结算、结算校验、前日汇总、周报、月报。
- 周报/月报已通过零覆盖场景验证：无数据时分别生成 `0/7`、`0/30` 覆盖率报告，并输出 `NO_REPLY`，不会打扰 Telegram。
- Phase 2C 最小闭环采用截图优先：已定义单张 Apple Watch / Apple Health 运动、活动、睡眠截图录入合同，并用 synthetic fixture 验证“已确认截图识别结果 → Markdown 日志 → expected 标准 JSON”的本地映射；暂不做历史批量导入或 parser。
- Phase 3A / C8 已定义一等跨维度 workflow 与报告 section contract，并用 synthetic fixture / validator 验证 sufficient 与 insufficient 两个分支；这是静态合同与 fixture 验证，不是 OpenClaw runtime 重新验证。

## 它能做什么

| 功能 | 说明 |
|------|------|
| **初始化健康档案** | 问答式收集年龄、性别、身高、体重、目标、活动水平，生成 `profile` 和 `goals` |
| **饮食记录** | 文字、食物照片、菜单截图 → 估算热量和宏量 → 写入当日日志 |
| **体重追踪** | 记录体重，计算 7 天均值、30 天趋势和目标差距 |
| **体检解读** | 识别体检报告照片或文字指标，标注异常，保存到 `workspace/medical/` |
| **运动/活动记录** | 记录手动运动描述，或从单张 Apple Watch / Apple Health 运动截图提取日期、类型、时长、active calories 和来源；活动摘要截图只记录日级步数/消耗 |
| **补剂管理** | 记录补剂和剂量，检查补剂-药物冲突，必要时给出安全提醒 |
| **睡眠记录** | 记录睡眠时长和质量，或从单张 Apple Watch / Apple Health 睡眠截图提取日期、时长和来源 |
| **跨维度洞察** | C8 静态合同和手动分析路径已定义，synthetic fixture 已验证；OpenClaw runtime smoke 待验证；基于 daily JSON 连接饮食、体重、运动/活动、睡眠，数据不足时固定不做关联判断，不输出因果、诊断或处方 |
| **自建食物库** | 从营养成分表照片提取数据，确认后写入个人食物库 |
| **目标更新** | 修改体重、热量、宏量目标，并重算 BMR/TDEE |
| **健康问答** | 基于仓库里的营养、医学、药物、补剂、运动、设备知识库回答问题 |
| **GLP-1 决策支持** | 评估是否符合药物干预条件，说明收益、风险和监测重点 |
| **训练计划** | 根据目标、伤病、器材和时间生成训练建议 |
| **睡眠分析** | 读取近期日志/JSON，分析睡眠时长、规律性和趋势 |

## 自动化已经接上

这些任务属于 OpenClaw runtime，不是系统 `crontab`。运行态真相见 [docs/openclaw-runtime.md](docs/openclaw-runtime.md)。

| 任务 | 时间 | 做什么 |
|------|------|--------|
| **零点结算** | 每天 00:05 | 读取昨日 Markdown 日志，生成结构化 JSON |
| **结算校验** | 每天 00:30 | 对比 Markdown 和 JSON 的热量/蛋白质，发现偏差时标注 |
| **前日汇总** | 每天 08:00 | 有 JSON 时生成 Telegram 摘要；无数据时 `NO_REPLY` |
| **周报** | 周一 08:30 | 统计上一个完整自然周，写入 `workspace/reports/` |
| **月报** | 每月 1 日 08:30 | 统计上一个完整自然月，写入 `workspace/reports/` |

## 它不做什么

- 不做食品条码扫描（薄荷健康做得更好）
- 不做实时运动追踪（Apple Watch 做得更好）
- 当前版本不做 Apple Health 历史批量导入
- 当前版本不做 Health Auto Export 自动同步
- 当前版本不做 Apple Health 原生 XML parser
- 不提供医疗诊断或处方
- 不在数据不足时硬编趋势结论

## 快速开始

### 1. Clone

```bash
git clone https://github.com/MochenRay/xiaoka-health-agent.git
cd xiaoka-health-agent
```

### 2. 可选：先建运行时目录

如果你的运行环境不会自动创建目录，先手动准备：

```bash
mkdir -p workspace/{logs,data,medical,reports,food-library}
printf '[]\n' > workspace/food-library/my-foods.json
```

### 3. 首次对话

在你的 AI 平台（OpenClaw / Claude Code 等）中加载本仓库，然后发送任意消息。小卡会自动检测到 profile 尚未配置，引导你完成初始化：

```
你：你好
小卡：你好！我是小卡，你的健康教练。
     检测到你还没有配置健康档案，我来帮你设置一下。
     你的身高是多少？（cm）
```

标准运行时约定见 [docs/phase1-minimum-contract.md](docs/phase1-minimum-contract.md)。仓库规范统一为：

- 用户档案：`config/profile.md`、`config/goals.md`
- 每日日志：`workspace/logs/YYYY-MM/DD.md`
- 结算 JSON：`workspace/data/YYYY-MM/DD.json`
- 体检/报告/食物库：`workspace/medical/`、`workspace/reports/`、`workspace/food-library/`

### 4. 开始使用

配置完成后，直接跟小卡对话即可：

```
你：午饭吃了一碗牛肉面加一个煎蛋
小卡：🍽️ 午餐记录
     | 食物 | 份量 | 热量 | 蛋白质 | 碳水 | 脂肪 |
     | 牛肉面 | 1碗 | 500 | 22g | 65g | 12g |
     | 煎蛋 | 1个 | 90 | 6g | 1g | 7g |
     | **小计** | | **590** | **28g** | **66g** | **19g** |

     📊 今日累计：590 / 1750 kcal（剩余 1160）
     🥩 蛋白质：28 / 150g（还差 122g）
```

## 目录结构

```
xiaoka-health-agent/
├── .env.example          ← 可选环境变量示例，不含真实密钥
├── agent.md              ← 小卡的人格设定（通用入口）
├── SOUL.md               ← 同 agent.md（OpenClaw 兼容）
├── IDENTITY.md           ← Agent 身份标识（OpenClaw 兼容）
├── SKILL.md              ← 技能路由和 Workflow 定义
├── references/           ← 知识库（营养/医学/药物/补剂/运动/设备）
├── config/               ← 配置模板（profile + goals）
├── templates/            ← 日志和报告模板
├── scripts/              ← Phase 2 工具脚本与 fixture 校验
├── workspace/            ← 用户数据（logs/data/medical/reports/food-library）
├── docs/                 ← PRD、路径合同、Schema、运行态规格、知识库来源
├── deploy/               ← 部署指南（OpenClaw / Claude Code）
└── plans/                ← 项目路线图、runtime smoke 与发布准备计划
```

## 运行时约定

Phase 1 的最小可用约定见 [docs/phase1-minimum-contract.md](docs/phase1-minimum-contract.md)。

重点只有两条：

- `config/` 放用户档案和目标，不放日志数据
- `workspace/` 放所有运行时健康数据，按月分目录存日志和 JSON

## 知识库来源

| 文件 | 来源 | 数据量 |
|------|------|--------|
| cn-food-db.json | 《中国食物成分表》标准版第 6 版 | 1,657 条基础食材 |
| nutrition.md | Mifflin-St Jeor, 中国居民膳食指南 | — |
| medical-markers.md | 临床医学指南 | CBC/代谢/血脂/甲状腺/FeNO/激素等 |
| medications.md | NEJM (STEP/SURMOUNT 试验) | GLP-1/减重药物决策框架 |
| supplements.md | WebMD, Harvard Health, PubMed | 三级循证分类 |
| exercise.md | ACSM, NSCA | 动作库 + 伤病安全标注 |
| cn-brands.md | AI 估算（仅供参考） | 中国品牌食品 ~600 条 |

详细验证记录见 [docs/knowledge-base-sources.md](docs/knowledge-base-sources.md)。

## 部署

- **OpenClaw**：[deploy/openclaw-setup.md](deploy/openclaw-setup.md)
- **Claude Code**：[deploy/claude-code-setup.md](deploy/claude-code-setup.md)

OpenClaw `cron` 运行态规格见 [docs/openclaw-runtime.md](docs/openclaw-runtime.md)。
周报/月报自动化规格见 [docs/report-automation.md](docs/report-automation.md)。

## Fixture 验证

仓库内 synthetic fixtures 不含个人健康数据：

```bash
python3 scripts/validate_phase2b_fixtures.py
python3 scripts/validate_phase2c_screenshot_fixtures.py
python3 scripts/validate_phase3a_c8_fixtures.py
```

Phase 2C fixture 只验证已确认截图识别结果的记录合同，不验证 OCR 质量、真实图片渲染、runtime 结算、Apple Health XML、Health Auto Export 或历史批量导入。

Phase 3A C8 fixture 只验证 synthetic fixture shape、报告 `## 跨维度观察` section wording，以及选定 source-backed metrics；不验证 OpenClaw runtime、真实报告生成器或个人健康数据。

## 模型选择

最低要求：

- 支持中文健康记录与较强的指令遵循
- 如需处理照片、截图、营养标签或体检单，必须支持图片输入
- Apple Watch / Apple Health 截图记录依赖可靠的 Vision/OCR；如果运行模型不能稳定读图，用户需要手动转写日期、来源、类型、时长、active calories 或睡眠时长等关键字段
- 能稳定遵守本仓库的文件读写路径合同

具体模型以部署环境可用项为准；OpenClaw 中可用 `openclaw agents list --bindings` 查看当前 `xiaoka` 配置。

## 隐私

- 所有健康数据默认存储在本地 `config/` 和 `workspace/` 目录，不上传任何服务器
- 使用云端模型 API 时，对话内容会发送给模型提供商（如阿里云、Moonshot 等）
- 如需完全离线使用，请部署本地模型

## 贡献

欢迎 PR：
- 补充/修正食物营养数据（cn-brands.md 或 cn-food-db.json）
- 补充体检指标（medical-markers.md）
- 改进 Workflow 设计（SKILL.md）

## 致谢

- [health-coach](https://github.com/MochenRay/health-coach) — 本项目脱胎于此
- [china-food-composition-data](https://github.com/Sanotsu/china-food-composition-data) — 中国食物成分表 JSON 数据

## License

MIT
