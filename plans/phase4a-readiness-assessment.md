# Phase 4A 启动前评估

> 最近更新：2026-05-27 CST
> 结论：Phase 4A 可以作为文档/发布打磨阶段启动，但不能把 runtime smoke 未完成
> 的能力写成已完成。

## 本轮 C 组结论

- 保守公开发布口径允许推进：可以先发布本地文件驱动 Agent、稳定路径合同、
  OpenClaw 自动化已接上、synthetic fixture validators 和清晰边界文档。
- 模型策略采用多模型口径：不固定推荐单一模型；截图、照片、营养标签和体检单图片工作流
  必须要求多模态/image-recognition/OCR 能力。
- D/E/F 外部集成与体验扩展暂停，Phase 4A 不实现 Apple Health XML parser、
  Health Auto Export、Withings/体脂秤、Telegram 快捷操作或静态 dashboard。
- 真实截图/OCR runtime smoke、C8 runtime smoke 和 M1/E1/S1 OpenClaw runtime 自动报告验证仍是后续项；
  公开文案不得写成 runtime-proven。

## 启动前必须先收口

- Phase 1 文档漂移：`docs/PRD.md`、README 目录树、Roadmap 基线需一致。
- 当前 runtime 基线：本地、`origin/main`、Mac Mini workspace 与五条 OpenClaw cron
  状态需有最新只读核验。
- Phase 3A smoke 路线：必须先记录是否要在公开发布前完成 C8 runtime smoke。

## 可先启动的 Phase 4A 工作

- 增加 `CHANGELOG.md`。
- 增加公开发布 checklist：`docs/public-release-checklist.md`。
- 跑 secret scan，并确认 `.env.example` 不含真实 token。
- 跑 Markdown link check 与现有 repository contract validator。
- 统一公开文案：区分已完成、static fixture verified、runtime verified、pending。
- 强化隐私与云端模型边界：`docs/privacy-and-medical-boundaries.md`。
- 强化医学免责声明：不诊断、不处方、不做药物调整。

## 不应阻塞 Phase 4A 启动的后续扩展

- Apple Health XML parser。
- Health Auto Export。
- Withings/体脂秤导入。
- Telegram 快捷操作。
- 静态 dashboard。
- M1/E1/S1 全量 runtime 自动报告验证。

这些是产品扩展，不是公开发布打磨的启动门槛；D/E/F 本轮已暂停或延后，README
不得把它们写成已完成。

## 发布前硬门槛

- `python3 scripts/validate_repository_contract.py`
- `python3 scripts/validate_daily_json_schema.py`
- `python3 scripts/validate_report_contracts.py`
- `python3 scripts/validate_phase2b_fixtures.py`
- `python3 scripts/validate_phase2c_screenshot_fixtures.py`
- `python3 scripts/validate_phase3a_c8_fixtures.py`
- `git diff --check`
- secret scan
- Markdown link check
- 若公开声称 C8 runtime 已闭环：先通过
  [phase3a-c8-runtime-smoke.md](phase3a-c8-runtime-smoke.md)
- 若公开声称真实截图/OCR 已闭环：先完成真实截图/OCR runtime smoke
