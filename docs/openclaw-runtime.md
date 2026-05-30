# OpenClaw Runtime 规格

本文件记录小卡在 OpenClaw 中运行时应遵守的公开合同。仓库 `git pull` 只同步文档和 Agent 包，不会自动修改 OpenClaw `cron` payload；凡修改 runtime 任务，必须先备份、再编辑、再验证。

## 真相层

| 层 | 说明 |
|----|------|
| 仓库 | Markdown/JSON Agent 包、模板、知识库和 synthetic fixtures |
| OpenClaw workspace | 由仓库同步得到的运行工作区 |
| OpenClaw runtime | `~/.openclaw/cron/jobs.json`，保存 cron job、schedule 和 payload |
| 用户健康数据 | `config/profile.md`、`config/goals.md`、`workspace/`，不进仓库 |

## 路径合同

运行态任务只能读写这些标准路径：

- `config/profile.md`
- `config/goals.md`
- `workspace/logs/YYYY-MM/DD.md`
- `workspace/data/YYYY-MM/DD.json`
- `workspace/medical/`
- `workspace/reports/`
- `workspace/food-library/my-foods.json`

新版任务不得读写旧根目录路径：

- `logs/`
- `data/`
- `medical/`
- `reports/`
- `food-library/`

## Cron 语义

| 任务 | 建议时间 | Delivery | 行为 |
|------|----------|----------|------|
| 零点结算 | 每天 00:05 | `none` | 读取昨日 Markdown 日志，生成昨日 JSON |
| 结算校验 | 每天 00:30 | `none` | 对比昨日 Markdown 与 JSON，必要时追加校验异常 |
| 前日汇总 | 每天 08:00 | `announce` | 有 JSON 时发送简短摘要；无数据时输出 `NO_REPLY` |
| 周报 | 周一 08:30 | `announce` | 统计上一个完整自然周，写入周报 |
| 月报 | 每月 1 日 08:30 | `announce` | 统计上一个完整自然月，写入月报 |

## 现有任务合同

### 零点结算

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`config/profile.md`、`config/goals.md`、`workspace/logs/{YYYY-MM}/{DD}.md`。
- 写入：`workspace/data/{YYYY-MM}/{DD}.json`。
- 若源日志不存在或无用户记录：静默跳过，不创建 JSON。
- 若源日志存在：按 `docs/data-schema.md` 生成结构化 JSON；目标文件可覆盖，保持幂等。
- 输出：`结算完成：YYYY-MM-DD` 或 `跳过：YYYY-MM-DD 无日志`。

### 结算校验

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`workspace/logs/{YYYY-MM}/{DD}.md` 与 `workspace/data/{YYYY-MM}/{DD}.json`。
- 任一文件不存在：静默跳过，不写入。
- 两者都存在时，对比热量和蛋白质等关键字段；偏差超过阈值时，在 Markdown 末尾追加校验异常。
- 输出：异常时 `校验异常：YYYY-MM-DD`；正常或缺文件时 `跳过：YYYY-MM-DD 无需校验`。

### 前日汇总

- 目标日期：`Asia/Shanghai` 时区的昨日。
- 读取：`workspace/data/{YYYY-MM}/{DD}.json` 与 `config/goals.md`。
- JSON 不存在：最终响应必须只有 `NO_REPLY`。
- JSON 存在：生成简短摘要。
- 汇总字段：体重、摄入、蛋白质、运动消耗、睡眠、一句话点评；缺失维度跳过。

### 周报和月报

- 周报统计上一个完整自然周，写入 `workspace/reports/weekly-YYYY-MM-DD.md`。
- 月报统计上一个完整自然月，写入 `workspace/reports/monthly-YYYY-MM.md`。
- 报告生成规则见 [report-automation.md](report-automation.md)。
- 覆盖率为 `0` 时仍写报告文件，但外部通知必须输出 `NO_REPLY`。
- 有效天数少于 `3` 天时，只做轻量回顾，不做趋势判断。

## 修改 runtime 前的硬门槛

- 先备份 `~/.openclaw/cron/jobs.json`。
- 若会写入 `workspace/data/` 或 `workspace/reports/`，先备份目标目录或目标文件。
- 确认本次是否会触发 `announce` delivery；可能触发外部通知时，先确认接收方和测试窗口。
- 不把真实 chat id、OAuth token、API 原始响应或个人健康数据写入仓库。
- `openclaw cron run` 只表示任务入队；必须再查运行历史终态，不能把入队当作成功。

## Runtime smoke planner

仓库提供 `scripts/plan_runtime_smoke.py` 作为 dry-run planner。它只读取
synthetic 或已脱敏的 `jobs.json` 形状，确认小卡五条任务、schedule、
delivery mode、`announce` 风险和受影响的标准路径，然后输出人工执行前的
备份、注入、运行历史检查与恢复步骤。

这个 planner 不会：

- SSH 到 Mac Mini。
- 调用 `openclaw cron run`、`openclaw cron edit` 或任何 OpenClaw 写命令。
- 修改 `~/.openclaw/cron/jobs.json`。
- 写入 `workspace/data/`、`workspace/reports/` 或 Telegram。

本地验证命令：

```bash
python3 scripts/validate_runtime_smoke_plan.py
python3 scripts/plan_runtime_smoke.py --jobs-json fixtures/synthetic/runtime-smoke/openclaw-jobs.json --scenario c8
```

若未来需要真实 runtime smoke，仍必须先确认测试窗口、接收方、备份路径和
回滚方式；尤其是 `前日汇总`、`周报`、`月报` 都可能触发 `announce`
delivery。

## Repo 同步与 runtime 同步

- 仓库同步：提交并推送 GitHub 后，在 OpenClaw workspace 执行 `git pull --ff-only origin main`。
- Runtime 同步：若需要修改 cron job、schedule 或 payload，单独编辑 `~/.openclaw/cron/jobs.json` 或使用 OpenClaw CLI，并按本文件硬门槛验证。
- 二者不能混为一个动作；`git pull` 不会自动改变 OpenClaw runtime。
