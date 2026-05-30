# Maintainer Memo

> 面向维护者的项目备忘。这里保存不适合放在 GitHub 首页的未完成事项和内部判断；README 只回答新用户最需要的三件事：能做什么、现在是什么样子、怎么开始使用。

## 可自主推进

- Google Health API repo 层 importer：当前已支持 synthetic / dry-run / ignored local
  output，已验证规范化、脱敏、幂等追加和不保存完整原始响应；后续可在同一记录合同上接真实 OAuth fetch。
- Runtime smoke planner：当前已能生成备份、注入、运行历史检查和恢复步骤，不自动运行
  OpenClaw cron，不触发 Telegram；后续可在确认测试窗口后扩成受控人工 runbook。
- 截图 fallback repo 层 fixtures：继续补充 synthetic 识别结果、缺字段和低置信度
  拒收场景；保持截图只是 fallback。
- 文档与公开口径校验：README 只保留 public contract，未完成项留在本 memo；
  `CHANGELOG.md`、`docs/PRD.md`、隐私边界和 validators 必须同步。

## 需要用户确认或真实 runtime 窗口

- Google Health API 真实 OAuth read/import smoke：需要用户 OAuth client、授权窗口和
  ignored token cache；不得把 token、账号标识、API 原始响应或真实健康数据写入仓库。
- C8 跨维度观察的真实自动周报/月报 runtime smoke：需要测试窗口、备份目录和
  Telegram `announce` 接收方确认。
- 药物、运动、睡眠深度分析的真实自动报告 runtime 验证：需先确认是否允许写入
  ignored `workspace/data/` 与 `workspace/reports/`，并在结束后恢复或归档。
- 真实截图/OCR runtime smoke：需要用户提供可测试截图或明确手动转写样本；低置信度
  和缺关键字段必须追问，不得编造。

## 暂缓或候选

- Apple Health XML、Health Auto Export、体脂秤导入、Telegram 快捷操作和静态数据看板。
- 这些项目不得写成当前能力；若恢复推进，先重新做 phase-plan 和 privacy / runtime
  boundary review。
