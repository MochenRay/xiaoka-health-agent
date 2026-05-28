# Runtime Smoke 边界

> 状态：边界说明。本文不表示任何 runtime smoke 已执行通过。

## 分层

| 层 | 可以在仓库内完成 | 不代表 |
|----|------------------|--------|
| Static contract | 校验 docs、templates、路径合同、`NO_REPLY`、C8 章节结构 | OpenClaw cron 已真实跑通 |
| Synthetic fixture | 校验 `fixtures/synthetic/` 的 daily JSON 与 expected report | 真实 OCR、真实个人数据质量 |
| Mac Mini pull acceptance | 确认 Mac Mini workspace fast-forward 到预期提交 | cron payload 已更新或 Telegram 已验证 |
| True runtime smoke | 在备份和回滚方案下运行 OpenClaw cron | 不应在无人确认时执行 |

## 本轮允许的 smoke

本轮只允许仓库侧 smoke：

- 读取仓库 fixtures。
- 运行 `scripts/validate_daily_json_schema.py`。
- 运行 `scripts/validate_report_contracts.py`。
- 运行既有 Phase 2B、Phase 2C、Phase 3A C8 fixture validators。
- 运行 `git diff --check`。

这些验证不得写 `~/.openclaw/cron/jobs.json`，不得写 runtime personal data，不得触发 Telegram。

## True Google Health API Ingestion Smoke

真实 Google Health API ingestion smoke 指使用用户已授权的 Google OAuth，只读拉取短日期窗口的
`steps`、`sleep` 和 `exercise`，把规范化结果写入 ignored `workspace/`，再检查日报、周报或
月报是否按既有数据门槛工作。

状态：read smoke 已在 2026-05-28 通过；importer/runtime 写入 smoke 未完成。

执行要求：

- 只能在用户明确确认 OAuth 授权和测试窗口后运行。
- 不打印、不保存 access token、refresh token、client secret、账号 email、health user id 或完整原始响应。
- 测试前备份会被写入的 `workspace/logs/`、`workspace/data/` 和 `workspace/reports/` 目标路径。
- 若触发 OpenClaw 周报/月报，先确认 Telegram delivery 行为。

## True OCR Runtime Smoke

真实截图/OCR runtime smoke 指使用真实 OpenClaw runtime，让截图识别结果进入
`workspace/logs/YYYY-MM/DD.md` 和 `workspace/data/YYYY-MM/DD.json`，再检查字段映射、
置信度和用户确认边界。

递延状态：降级为 fallback 测试，不再作为运动、步数、睡眠设备数据的主路径。

递延原因：

- 可能涉及真实截图或个人健康数据。
- OCR/Vision 模型选择会影响识别质量，但不改变仓库路径合同。
- 低置信度结果需要用户确认，不能由无人值守测试自动写入。
- 若 delivery 为 announce，可能触发 Telegram。

## True C8 Runtime Smoke

真实 C8 runtime smoke 指运行 Mac Mini OpenClaw 周报/月报 cron，让真实 runtime
生成报告，并验证 `## 跨维度观察`、`### 结论`、`### 依据`、`### 边界` 与数据门槛。

递延状态：递延到用户集中测试。

递延原因：

- 需要备份目标 `workspace/data/`、`workspace/reports/` 和 `~/.openclaw/cron/jobs.json`。
- 周报/月报 delivery 可能向 Telegram 发摘要。
- synthetic C8 validator 只能证明 static contract，不等于 runtime-proven。

## Personal Data Improvements

以下内容全部递延到用户集中测试，不由仓库侧 validator 或 pull 验收写入：

- 更多个人基线数据。
- 自建食物库扩充。
- 运动、睡眠和长期趋势样本积累。
- 真实截图/OCR 纠错记录。
- Google Health API token refresh、导入幂等和字段映射。
- 任何可识别个人的健康资料。

## Runtime 执行前硬门槛

进入 true runtime smoke 前必须满足：

- 用户确认测试窗口与 Telegram 行为。
- 备份 `~/.openclaw/cron/jobs.json`。
- 备份所有会被覆盖的 `workspace/data/` 和 `workspace/reports/` 目标路径。
- 只写 synthetic fixture 或用户明确提供的测试数据。
- 记录 run id、status、summary 形态、报告路径和覆盖率；不记录真实 chat id 或个人健康明细。
- 执行后删除 synthetic JSON，并恢复或归档被覆盖报告。
