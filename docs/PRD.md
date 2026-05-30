# Xiaoka Health Agent 范围合同

> 最近更新：2026-05-30 CST
> 本文件说明当前仓库的产品范围和公开表述边界。旧计划和执行过程不在仓库中并列维护；如需追溯，使用 Git history。

## 产品定位

小卡是本地文件驱动的 AI 健康教练 Agent 包。它不做后端服务，也不替代 Apple Health、薄荷健康、医院系统或医生；它负责把健康档案、饮食、体重、运动、睡眠、补剂和体检记录整理到本地 `config/` 与 `workspace/`，并用 AI 做结构化记录、解释和低断言强度分析。

## 当前已建立

- Phase 1 最小可用合同：初始化、记录、目录结构和写入纪律已定义，见 [phase1-minimum-contract.md](phase1-minimum-contract.md)。
- OpenClaw runtime 合同：日结算、结算校验、前日汇总、周报和月报的路径与行为已定义，见 [openclaw-runtime.md](openclaw-runtime.md)。
- 周报/月报报告合同：覆盖率、`NO_REPLY`、补结算和 C8 接入规则已定义，见 [report-automation.md](report-automation.md)。
- Google Health API 方向：人工 OAuth read smoke 已证明可读取 HealthKit 来源的步数、睡眠和运动数据；repo 层 importer v1 已有 synthetic proof，见 [google-health-api-ingestion.md](google-health-api-ingestion.md)。
- C8 跨维度观察：静态报告合同和 synthetic sufficient/insufficient fixtures 已建立，见 [c8-cross-dimensional-insights.md](c8-cross-dimensional-insights.md)。
- M1/E1/S1 深度分析：repo 层结构化摘要合同、模板入口和 synthetic expected sections 已建立，见 [deep-analysis-report-contract.md](deep-analysis-report-contract.md)。
- Runtime smoke planner：dry-run planner 已能基于 synthetic `jobs.json` 输出备份、注入、运行历史检查和恢复步骤；不运行 OpenClaw cron。

## 当前未完成

- Google Health API 真实 OAuth fetch、token refresh、ignored token cache 和 OpenClaw runtime 同步。
- 真实截图/OCR runtime smoke；截图路径仅作为 fallback。
- C8 跨维度观察的真实自动周报/月报 runtime smoke。
- M1/E1/S1 深度分析的真实自动报告 runtime 验证。
- Apple Health XML、Health Auto Export、体脂秤导入、Telegram 快捷操作和静态数据看板。

## 明确不做

- 不做食品条码扫描。
- 不做实时运动追踪。
- 不做医疗诊断、处方或药物调整。
- 数据不足时不硬编趋势、因果或跨维度结论。
- 不把个人健康数据、OAuth token、API 原始响应或真实 Telegram 目标写进仓库。

## 公开表述边界

可说：

- 小卡是本地文件驱动的健康 Agent 包。
- 核心 workflow、OpenClaw 五类定时任务、周报/月报合同、Google Health API read smoke、Google Health API repo 层 importer synthetic proof、截图 fallback mapping fixture、C8 静态合同均已建立。
- 仓库内的 synthetic fixtures 可用于验证 repo 层合同和示例数据结构。

不可说：

- Google Health API 真实自动同步已完成。
- 真实截图识别已完成。
- Apple Health 文件式历史同步已完成。
- C8 runtime 报告已完整闭环。
- 医学趋势分析可替代医生判断。
