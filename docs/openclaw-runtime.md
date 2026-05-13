# OpenClaw Runtime 规格

> 最近核验：2026-05-13 PDT
> 仓库基线：`main` / `1967ae4`
> Mac Mini workspace：`~/.openclaw/workspace-xiaoka` / `main` / `1967ae4`
> Runtime 真相层：Mac Mini 上的 `~/.openclaw/cron/jobs.json`

本文件记录小卡在 OpenClaw 中的运行态合同。仓库 `git pull` 只同步文档和 Agent 包，不会自动修改 OpenClaw `cron` payload；凡改 `cron`，必须单独走运行态备份、编辑和验证。

## 真相层

| 层 | 位置 | 说明 |
|----|------|------|
| 仓库真相层 | `/Users/rayli/xiaoka-health-agent` | Markdown/JSON Agent 包 |
| GitHub 同步层 | `origin/main` | 本地改动先 commit/push |
| OpenClaw workspace | `mac-mini:~/.openclaw/workspace-xiaoka` | 通过 `git pull --ff-only origin main` 同步 |
| OpenClaw runtime | `mac-mini:~/.openclaw/cron/jobs.json` | `cron` job、schedule、payload 的最终真相 |
| 用户健康数据 | `config/profile.md`、`config/goals.md`、`workspace/` | 被 `.gitignore` 排除，不进仓库 |

## 路径合同

运行态任务只能读写这些标准路径：

- `config/profile.md`
- `config/goals.md`
- `workspace/logs/YYYY-MM/DD.md`
- `workspace/data/YYYY-MM/DD.json`
- `workspace/medical/`
- `workspace/reports/`
- `workspace/food-library/my-foods.json`

禁止把新版任务指向旧根目录路径：

- `logs/`
- `data/`
- `medical/`
- `reports/`
- `food-library/`

## 当前 Cron Jobs

| 名称 | ID | Schedule | Delivery | Agent | 状态 |
|------|----|----------|----------|-------|------|
| 零点结算 | `f6f9f188-6010-459a-ae67-f8300d164466` | `5 0 * * * @ Asia/Shanghai` | `none -> telegram:<chat_id>` | `xiaoka` | 已存在 |
| 结算校验 | `31478134-17c9-4058-90cb-d68a0fd58c42` | `30 0 * * * @ Asia/Shanghai` | `none -> telegram:<chat_id>` | `xiaoka` | 已存在 |
| 前日汇总 | `81d3e9d4-fc76-4b08-8f33-6e533334bbb8` | `0 8 * * * @ Asia/Shanghai` | `announce -> telegram:<chat_id>` | `xiaoka` | 已存在 |
| 周报 | 未创建 | 建议 `30 8 * * 1 @ Asia/Shanghai` | 建议 `announce` | `xiaoka` | 计划中 |
| 月报 | 未创建 | 建议 `30 8 1 * * @ Asia/Shanghai` | 建议 `announce` | `xiaoka` | 计划中 |

## 现有 Job 合同

### 零点结算

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`config/profile.md`、`config/goals.md`、`workspace/logs/{YYYY-MM}/{DD}.md`。
- 写入：`workspace/data/{YYYY-MM}/{DD}.json`。
- 若源日志不存在或无用户记录：静默跳过，不创建 JSON。
- 若源日志存在：按 `docs/data-schema.md` 生成结构化 JSON；目标文件可覆盖，保持幂等。
- 输出：`结算完成：YYYY-MM-DD` 或 `跳过：YYYY-MM-DD 无日志`。
- `timeoutSeconds`: `240`。

### 结算校验

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`workspace/logs/{YYYY-MM}/{DD}.md` 与 `workspace/data/{YYYY-MM}/{DD}.json`。
- 任一文件不存在：静默跳过，不写入。
- 两者都存在时：
  - 对比 JSON `nutrition.total_calories` 与 Markdown 餐次热量合计。
  - 对比 JSON `nutrition.protein_g` 与 Markdown 餐次蛋白质合计。
  - 热量偏差超过 `10%` 时，在 Markdown 末尾追加校验异常。
  - 蛋白质偏差超过 `20%` 时，在 Markdown 末尾追加校验异常。
- 输出：异常时 `校验异常：YYYY-MM-DD`；正常或缺文件时 `跳过：YYYY-MM-DD 无需校验`。
- `timeoutSeconds`: `180`。

### 前日汇总

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`workspace/data/{YYYY-MM}/{DD}.json` 与 `config/goals.md`。
- JSON 不存在：最终响应必须只有 `NO_REPLY`。
- JSON 存在：生成不超过 10 行的 Telegram 摘要。
- 汇总字段：体重、摄入、蛋白质、运动消耗、睡眠、一句话点评；缺失维度跳过。
- Delivery 为 `announce`，因此无数据分支必须使用 `NO_REPLY` 避免噪音。
- `timeoutSeconds`: `180`。

## 改 Runtime 前置步骤

先备份 `jobs.json`：

```bash
ssh mac-mini 'cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.bak-$(date +%Y%m%d-%H%M%S)'
```

只读检查：

```bash
ssh mac-mini 'openclaw cron list'
ssh mac-mini 'openclaw cron show f6f9f188-6010-459a-ae67-f8300d164466'
ssh mac-mini 'openclaw cron show 31478134-17c9-4058-90cb-d68a0fd58c42'
ssh mac-mini 'openclaw cron show 81d3e9d4-fc76-4b08-8f33-6e533334bbb8'
```

编辑后验证：

```bash
ssh mac-mini 'openclaw cron run <id>'
ssh mac-mini 'openclaw cron runs --id <id> --limit 1'
ssh mac-mini 'openclaw cron list'
```

`openclaw cron run` 只表示任务已入队，不能当作成功证据；必须再看 `openclaw cron runs --id ...` 的最终记录。

## Repo 同步流程

本机仓库侧改动：

```bash
git diff --check
git status --short
git commit -m "<message>"
git push origin main
```

Mac Mini workspace 同步：

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git pull --ff-only origin main'
```

同步后抽查：

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git rev-parse --short HEAD'
ssh mac-mini 'openclaw cron list | grep xiaoka'
```

## 后续新增周报/月报

周报、月报的仓库侧规格见 [report-automation.md](report-automation.md)。

落地 runtime 前必须确认：

- 已备份 `~/.openclaw/cron/jobs.json`。
- 周报 schedule 为周一早上，统计上一个完整自然周。
- 月报 schedule 为每月 1 日早上，统计上一个完整自然月。
- 无数据分支输出 `NO_REPLY`，避免 Telegram 噪音。
- 用无数据与样例数据两类场景检查 `openclaw cron runs --id ...`。
