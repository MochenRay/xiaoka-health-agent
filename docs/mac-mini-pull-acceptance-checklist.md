# Mac Mini Pull 验收清单

> 状态：仓库侧验收清单。本文不执行 SSH、不运行 OpenClaw cron、不修改
> `~/.openclaw/cron/jobs.json`，也不写入个人运行时数据。

## 适用范围

本清单用于本地仓库提交后，让 Mac Mini 的
`~/.openclaw/workspace-xiaoka` 只做代码同步验收。它验证 pull 是否把仓库真相层
同步到 OpenClaw workspace，不验证真实 OCR、真实 C8 runtime、Telegram delivery
或个人健康数据质量。

## Pull 前

- 本地分支已完成仓库侧验证，至少包括 `git diff --check` 和相关 validator。
- 待同步提交已进入目标远端分支。
- 明确本轮只是 `git pull --ff-only`；不编辑 `~/.openclaw/cron/jobs.json`。
- 确认不会覆盖 `config/profile.md`、`config/goals.md` 或 `workspace/` 下的个人运行时数据。
- 若后续要运行 cron，先另开 runtime smoke 步骤，并确认 Telegram 接收方、时间窗口和回滚方案。

## Pull 操作

建议命令：

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git fetch origin && git status --short --untracked-files=no && git pull --ff-only origin main'
```

验收只接受 fast-forward。若出现本地 tracked 变更、merge commit 需求或冲突，停止并先审计差异，不在 runtime 上临时修补。

## Pull 后只读验收

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git rev-parse --short HEAD && git status --short --untracked-files=no'
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && python3 scripts/validate_repository_contract.py'
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && python3 scripts/validate_daily_json_schema.py'
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && python3 scripts/validate_report_contracts.py'
```

通过标准：

- Mac Mini workspace HEAD 等于预期提交。
- tracked files clean；OpenClaw 注入的未跟踪 overlay 不作为失败项。
- 仓库 validator 全部通过。
- 未修改 `~/.openclaw/cron/jobs.json`。
- 未新增、覆盖或复制个人 `workspace/` 数据。
- 未触发 Telegram。

## 明确递延

- 真实截图/OCR runtime smoke：递延到用户集中测试。
- C8 runtime smoke：递延到用户集中测试；仓库侧 C8 validator 只证明 static contract 和 synthetic fixture。
- 个人基线数据、食物库、运动/睡眠长期样本补充：递延到用户集中测试，不由 pull 验收写入。

## 记录格式

记录 pull 验收时只写：

- 预期提交与 Mac Mini HEAD。
- `git status --short --untracked-files=no` 结果。
- validator 命令与通过/失败状态。
- 是否确认未改 cron、未写 personal data、未触发 Telegram。
