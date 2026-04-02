# 小卡健康 Agent

开源 AI 健康教练——血检解读、补剂管理、GLP-1 决策、饮食追踪、跨维度健康趋势分析。数据本地存储。

## 它能做什么

| 功能 | 说明 |
|------|------|
| **饮食记录** | 文字/图片输入 → 热量核算 → 每日累计 → 剩余预算 |
| **体重追踪** | 记录 → 7天均值 → 30天趋势 → 目标进度 → 异常检测 |
| **体检解读** | 照片/文字 → 逐项解读 → 异常标注 → 历史对比 |
| **补剂管理** | 三级循证推荐 → 交互作用检查 → 服用时机 |
| **运动记录** | Apple Health 截图/手动输入 → 消耗计算 |
| **周报/月报** | 提供模板；自动汇总依赖部署侧 Cron |

## 它不做什么

- 不做食品条码扫描（薄荷健康做得更好）
- 不做实时运动追踪（Apple Watch 做得更好）
- 不提供医疗诊断或处方

## 快速开始

### 1. Clone

```bash
git clone https://github.com/你的用户名/xiaoka-health-agent.git
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
├── agent.md              ← 小卡的人格设定（通用入口）
├── SOUL.md               ← 同 agent.md（OpenClaw 兼容）
├── IDENTITY.md           ← Agent 身份标识（OpenClaw 兼容）
├── SKILL.md              ← 技能路由和 Workflow 定义
├── references/           ← 知识库（营养/医学/药物/补剂/运动/设备）
├── config/               ← 配置模板（profile + goals）
├── templates/            ← 日志和报告模板
├── scripts/              ← 预留：Phase 2 工具脚本（当前仅占位说明）
├── workspace/            ← 用户数据（logs/data/medical/reports/food-library）
├── docs/                 ← PRD + Schema + 知识库来源
└── deploy/               ← 部署指南（OpenClaw / Claude Code）
```

## 运行时约定

Phase 1 的最小可用约定见 [docs/phase1-minimum-contract.md](docs/phase1-minimum-contract.md)。

重点只有两条：

- `config/` 放用户档案和目标，不放日志数据
- `workspace/` 放所有运行时健康数据，按月分目录存日志和 JSON

## 知识库来源

| 文件 | 来源 | 数据量 |
|------|------|--------|
| cn-food-db.json | 《中国食物成分表》标准版第 6 版 | 1,677 条基础食材 |
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

## 推荐模型

| 模型 | 多模态 | 中文 | 说明 |
|------|--------|------|------|
| qwen3.5-plus | ✅ | ✅ | 推荐：原生多模态，中文优秀 |
| kimi-k2.5 | ✅ | ✅ | 备选：多模态+视觉推理强 |
| Claude | ✅ | ✅ | 推理质量最高 |

最低要求：支持多模态（图片输入）的模型。纯文本模型可用但无法处理截图。

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
