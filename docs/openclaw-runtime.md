# OpenClaw Runtime 规格

> 最近核验：2026-05-24 CST
> 仓库基线：`main` / `9dc598f`
> Mac Mini workspace：`~/.openclaw/workspace-xiaoka` / `main` / `9dc598f`
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

## 当前部署快照

- Gateway process 正在运行；2026-05-24 核验时默认 IPv4 loopback
  `127.0.0.1:18789` 连接报 `EADDRNOTAVAIL`，`localhost` / `::1` 可访问。
  临时运行 CLI 时需使用 `--url 'ws://[::1]:18789' --token <gateway-token>`。
- Agent ID：`xiaoka`。
- 当前模型：`openai/gpt-5.4`。
- OpenClaw workspace tracked files clean；存在 `.openclaw/`、`AGENTS.md`、`MEMORY.md` 等未跟踪 runtime overlay，属 OpenClaw 本地注入层。

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
| 零点结算 | `f6f9f188-6010-459a-ae67-f8300d164466` | `5 0 * * * @ Asia/Shanghai` | `none -> telegram:<chat_id>` | `xiaoka` | 已启用，最近运行 `ok` |
| 结算校验 | `31478134-17c9-4058-90cb-d68a0fd58c42` | `30 0 * * * @ Asia/Shanghai` | `none -> telegram:<chat_id>` | `xiaoka` | 已启用，最近运行 `ok` |
| 前日汇总 | `81d3e9d4-fc76-4b08-8f33-6e533334bbb8` | `0 8 * * * @ Asia/Shanghai` | `announce -> telegram:<chat_id>` | `xiaoka` | 已启用，最近运行 `ok` |
| 周报 | `961c8fcb-9f52-4842-94f6-720202ffa5b2` | `30 8 * * 1 @ Asia/Shanghai` | `announce -> telegram:<chat_id>` | `xiaoka` | 已启用，最近运行 `ok` |
| 月报 | `51522e31-54dd-495e-8c0e-e8432bb75acd` | `30 8 1 * * @ Asia/Shanghai` | `announce -> telegram:<chat_id>` | `xiaoka` | 已启用，最近运行 `ok` |

## 最近运行态验证

2026-05-24 CST 核验：

- 本地 `main`、`origin/main`、Mac Mini workspace 均为 `9dc598f`。
- Mac Mini 直接 `git pull --ff-only origin main` 因外网 443/22 不通失败；本次通过
  `git bundle` 经 SSH 传输并 fast-forward 到 `9dc598f`，同时更新了
  `refs/remotes/origin/main`。
- `openclaw cron list` 中五条小卡任务均 enabled，最近运行状态均为 `ok`。
- 2026-05-24 的日结算/校验/前日汇总因 2026-05-23 无日志或 JSON 而静默跳过；这符合“无数据不打扰”的当前合同。
- 当前 reports 文件：`workspace/reports/weekly-2026-05-10.md`、`workspace/reports/weekly-2026-05-17.md`、`workspace/reports/monthly-2026-04.md`，均为零覆盖报告。
- Mac Mini 仍存在旧根目录 `logs/`、`data/`；其中 `2026-03-26` 日志/JSON 与标准 `workspace/` 副本 hash 相同。旧目录只作为 legacy 层看待，后续清理前需备份。

2026-05-24 Phase 2B synthetic runtime 验证尝试：

| 尝试 | 备份目录 | 结果 | 清理 |
|------|----------|------|------|
| 第一次 | `/Users/ray/.openclaw/backups/xiaoka-phase2b-synthetic-20260524-180535` | 默认 CLI 走 `127.0.0.1:18789`，gateway 连接 `EADDRNOTAVAIL`；cron 未实际执行 | synthetic JSON 已删除，原零覆盖报告已恢复 |
| 第二次 | `/Users/ray/.openclaw/backups/xiaoka-phase2b-synthetic-20260524-181001` | 改用 `ws://[::1]:18789` 后周报入队并运行，但模型请求 `https://chatgpt.com/backend-api/codex/responses` stream disconnected；月报未继续执行 | synthetic JSON 已删除，原零覆盖报告已恢复 |

结论：仓库 fixture 与 Mac Mini workspace 已就绪，但非零 runtime 验证未通过。阻塞项是
Mac Mini 当前外网不可达：`github.com:443`、`chatgpt.com:443`、`apple.com:443`
均连接失败。修复 Mac Mini 网络/代理后，按 [report-automation.md](report-automation.md)
重跑 synthetic 验证。

2026-05-13 PDT 已在 Mac Mini 上备份并启用周报、月报任务。启用前备份：

```text
mac-mini:~/.openclaw/cron/jobs.json.bak-20260513-194637-before-enable
```

手动运行结果：

| 名称 | Run ID | Status | Duration | Summary | Delivery | 生成文件 |
|------|--------|--------|----------|---------|----------|----------|
| 周报 | `manual:961c8fcb-9f52-4842-94f6-720202ffa5b2:1778672830235:5` | `ok` | `61093ms` | `NO_REPLY` | `not-delivered` | `workspace/reports/weekly-2026-05-10.md` |
| 月报 | `manual:51522e31-54dd-495e-8c0e-e8432bb75acd:1778672906326:6` | `ok` | `103683ms` | `NO_REPLY` | `not-delivered` | `workspace/reports/monthly-2026-04.md` |

两次手动运行均为零覆盖场景：runtime 生成 `0/N` 报告文件，但 Telegram fallback 未发送。`workspace/reports/` 属于运行态数据目录，被 `.gitignore` 排除，不进入仓库。

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

## Phase 2B Synthetic 非零验证待执行

仓库已定义 Phase 2B synthetic fixture，用于验证周报/月报非零覆盖分支。
截至本记录，本节只定义执行规范，不表示 Mac Mini runtime 已完成 synthetic
验证。

- fixture 来源：`fixtures/synthetic/phase2b/workspace/data/`
- marker：每个 JSON 的 `notes` 必须包含 `SYNTHETIC_PHASE2B`
- 周报目标：`2026-05-11..2026-05-17` 覆盖率 `3/7`
- 月报目标：`2026-04` 覆盖率 `3/30`
- 执行规范：见 [report-automation.md](report-automation.md) 的
  “Phase 2B Mac Mini 安全验证步骤”

执行前必须备份 `~/.openclaw/cron/jobs.json`、`workspace/data/2026-04`、
`workspace/data/2026-05` 以及会被覆盖的 `workspace/reports/weekly-2026-05-17.md`
和 `workspace/reports/monthly-2026-04.md`。写入 synthetic fixture 前必须检查目标
日期 JSON 不存在；若存在则停止，不覆盖真实记录。因为周报、月报 delivery 为
`announce`，手动运行可能发送 Telegram；记录验证结果时不得写真实 chat id，不得
把 synthetic fixture 和真实健康数据混合归档。验证后必须把 generated report 归档到
备份目录，并恢复原报告文件。
