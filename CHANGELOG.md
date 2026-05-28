# Changelog

本文件记录公开发布口径下可以稳定描述的能力、验证证据和仍待 runtime
smoke 的项目。公开 README、发布页和对外介绍应以本文件与发布 checklist 为边界。

## Unreleased - Google Health API ingestion decision

日期：2026-05-28 CST

### Changed

- 运动、步数和睡眠设备数据的主接入路径改为 Google Health API。
- Apple Watch / Apple Health 截图从主路径降级为 fallback；既有 Phase 2C synthetic
  fixture 只继续证明截图识别结果到 daily JSON 的 mapping。
- README、PRD、SKILL、数据 schema、隐私边界、runtime smoke 边界和发布 checklist
  已同步该口径。

### Verified

- 通过人工 OAuth read smoke 验证 Google Health API 可读取 `identity`、`steps`、
  `sleep` 和 `exercise`。
- 返回来源包含 HealthKit / Apple 来源，证明 iOS Apple Health 经 Google Health API
  的读取路径可行。

### Pending

- 正式 OAuth client 配置、token refresh、本地 token cache、导入脚本、幂等写入和
  OpenClaw runtime smoke 尚未实现。
- 不得把本次人工验证中的 token、账号标识、原始响应或真实健康明细写入仓库。

## Unreleased - Phase 4A release hardening

日期：2026-05-27 CST

### Public-ready capabilities

- 小卡是本地文件驱动的 AI 健康教练 Agent 包，不是后端服务。
- 核心本地路径合同已稳定：`config/` 保存用户档案和目标，`workspace/`
  保存日志、结算 JSON、体检材料、报告和个人食物库。
- Agent 核心工作流可公开描述为已可用：初始化、饮食记录、体重追踪、
  运动/活动记录、睡眠记录、补剂管理、体检解读、目标更新、自建食物库和
  健康问答。
- OpenClaw 自动化可公开描述为已接上：零点结算、结算校验、前日汇总、周报和
  月报。公开文案仍需区分 runtime 已启用、fixture 已验证和真实 smoke 未完成。
- Phase 2B synthetic 周报/月报 fixtures 已有 validator，可验证报告 shape 与
  zero/non-zero fixture 行为。
- Phase 2C 截图先行路径已验证的是“已确认识别结果 -> Markdown 日志 ->
  expected daily JSON”的 synthetic mapping，不是 OCR 质量或真实截图 runtime。
- Phase 3A C8 已有一等 workflow、报告 section contract 和 sufficient /
  insufficient synthetic validator；这仍是 static fixture validation，不是
  OpenClaw runtime smoke。
- Phase 3B M1/E1/S1 已有 repo 层结构化摘要合同、周/月报模板入口、synthetic
  daily JSON fixture 和 expected report sections；这仍是 static fixture validation，
  不是 OpenClaw runtime 自动报告验证。
- 结算 JSON prompt 已有 repo 层 synthetic regression fixture，可校验 fabricated
  daily Markdown log 到 expected daily JSON 的合同；这不是 OpenClaw runtime 结算验证。
- 仓库公开边界已补齐：发布 checklist、隐私与云端模型边界、医学非诊断边界和
  screenshot/OCR 限制。

### Model strategy

- Xiaoka 支持多模型部署；模型选择是 runtime 绑定，不改变仓库路径合同。
- 文字记录、报告整理和 fixture validators 不依赖固定模型名称。
- 截图、食物照片、营养标签和体检单图片工作流必须使用支持图片输入、图片识别或
  OCR 的多模态模型。若运行模型不能可靠读图，用户必须手动转写关键字段。
- 本仓库不把任何单一模型写成固定推荐；公开发布前只声明能力要求，并按部署环境
  重新核验。

### Pending runtime smoke items

- 真实 Apple Watch / Apple Health 截图 OCR runtime smoke 仍未完成。
- 更完整的截图回归 fixtures 仍未完成。
- C8 OpenClaw runtime smoke 仍未完成。
- M1/E1/S1 OpenClaw runtime 自动报告验证仍未完成；不得写成 runtime-proven。
- Apple Health XML parser、Health Auto Export、Withings/体脂秤导入、Telegram
  快捷操作和静态 dashboard 已延后；不得写成 Phase 4A 发布能力。
- 公开发布或打 tag 前仍需重新运行 secret scan、Markdown 链接/仓库合同校验、
  settlement prompt / daily JSON / report contract validators、fixture validators
  和 whitespace 检查。
