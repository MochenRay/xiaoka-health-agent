# 小卡剩余 61 项依赖待办清单

> 生成基线：2026-05-27 CST，`main` / `f430ee0`
> 当前裁剪：真实 OCR/C8 runtime smoke、个人基线和自建食物库补充等需用户介入项，先递延到用户集中测试；D/E/F 组整体挂起。
> 来源：`plans/xiaoka-project-roadmap-checklist.md` 中全部未勾选项，共 61 项。
> 说明：本清单保留 Roadmap 的 61 个未完成映射；若多项同义或重复，实施时可用同一个切片同时关闭多处来源。

## 依赖顺序

1. 先补 runtime smoke 与可回归测试底座。
2. 再接深度分析能力，因为 M1/E1/S1、C8 runtime 都依赖稳定 daily JSON、报告 prompt 和样例。
3. 再做 Phase 4A 发布打磨，避免公开文案超过真实实现。
4. 最后推进数据集成、体验命令和可视化扩展。

## A. Runtime Smoke 与测试底座

- [ ] R01. 完成真实截图/OCR runtime 验证，并补更完整回归 fixtures。来源：Roadmap L59。
  - Worker A 2026-05-27：真实 OCR runtime smoke 递延到用户集中测试；本轮只补仓库侧 fixture/schema validator 与边界文档，见 `docs/runtime-smoke-boundary.md`。
- [ ] R02. 执行“真实截图/OCR runtime smoke”这个当前最佳下一步。来源：Roadmap L452。
  - Worker A 2026-05-27：不运行真实 OpenClaw cron、不触发 Telegram；执行条件记录在 `docs/runtime-smoke-boundary.md`。
- [x] R03. 积累或构造足够运动/睡眠结构化 JSON，作为趋势自动化输入。来源：Roadmap L181。
  - 2026-05-27：已以 non-private synthetic daily JSON 覆盖 exercise/sleep/C8/deep-analysis 输入；真实个人数据仍递延到用户集中测试。
- [x] R04. 增加非私人路径下的样例数据。来源：Roadmap L289。
  - 2026-05-27：已新增 `fixtures/synthetic/phase3b-deep-analysis/`，并纳入 daily JSON schema validator。
- [x] R05. 增加测试样例，让结算/报告 prompt 可安全迭代。来源：Roadmap L182。
  - 2026-05-27：已新增 M1/E1/S1 synthetic 示例与 report contract validator；结算 prompt 的真实 runtime 回归仍未执行。
- [ ] R06. 增加结算 JSON 的 prompt 回归测试。来源：Roadmap L438。
- [x] R07. 增加 JSON schema validation。来源：Roadmap L439。
  - Worker A 2026-05-27：已新增 `scripts/validate_daily_json_schema.py`，覆盖 non-private synthetic daily JSON fixture 的日期、可选对象/null 字段、关键数值字段与 synthetic/no-real-person 合同。
- [ ] R08. 增加 Mac Mini OpenClaw runtime smoke test 脚本。来源：Roadmap L435。
  - Worker A 2026-05-27：runtime smoke 脚本未实现；本轮只冻结执行边界，true OCR/C8 runtime smoke 递延到用户集中测试。
- [x] R09. 增加 Mac Mini OpenClaw pull 后的人工验收 checklist。来源：Roadmap L290。
  - Worker A 2026-05-27：已新增 `docs/mac-mini-pull-acceptance-checklist.md`，限定 pull 验收为 fast-forward 与仓库 validator，不改 cron、不写 personal data、不触发 Telegram。
- [x] R10. 明确模型选择只影响 OCR/Vision 质量，不改变仓库路径合同。来源：Roadmap L188。
  - 2026-05-27：README 与隐私/医学边界文档已改为多模型口径；截图/照片能力必须具备多模态/image-recognition/OCR。
- [x] R11. 重新核验模型推荐区，尤其多模态能力；当前 runtime 模型为 `openai/gpt-5.4`。来源：Roadmap L237。
  - 2026-05-27：公开文案不再固定推荐单一模型，只写能力要求。
- [x] R12. 公开发布前重新核验当前模型推荐。来源：Roadmap L142。
  - 2026-05-27：用户确认模型策略为“支持多模型，但截图能力必须具备多模态图像识别”。
- [ ] R13. 重新验证跨维度洞察 runtime，包括真实截图/OCR runtime smoke、C8 runtime smoke 和长期趋势。来源：Roadmap L61。
  - Worker A 2026-05-27：本轮新增 `scripts/validate_report_contracts.py` 仅验证 static report contract；runtime 与长期趋势仍递延到用户集中测试。
- [ ] R14. 执行“C8 runtime smoke”这个当前最佳下一步。来源：Roadmap L453。
  - Worker A 2026-05-27：C8 runtime smoke 未执行；边界与准入条件见 `docs/runtime-smoke-boundary.md`。
- [ ] R15. 完成真实 runtime C8 验证。来源：Roadmap L377。
  - Worker A 2026-05-27：未完成真实 runtime C8；当前只保持 synthetic/static proof。
- [ ] R16. 用 C8 runtime smoke 验证报告模板达到 runtime-proven。来源：Roadmap L179。
  - Worker A 2026-05-27：报告模板由 `scripts/validate_report_contracts.py` 做 static contract gate，runtime-proven 仍待用户集中测试。
- [ ] R17. 验证真实 runtime 中有足够数据时，周报/月报包含有用跨维度分析。来源：Roadmap L383。
- [ ] R18. 验证真实 runtime 中覆盖率太低时，Agent 不做趋势断言。来源：Roadmap L384。
- [ ] R19. 补更多个人基线数据以提升建议质量。来源：Roadmap L186。
  - Worker A 2026-05-27：个人基线数据补充递延到用户集中测试；本轮不写 runtime personal data。
- [ ] R20. 补更多自建食物库数据以提升饮食精度。来源：Roadmap L187。
  - Worker A 2026-05-27：自建食物库补充递延到用户集中测试；本轮不写 `workspace/food-library/`。

## B. 深度分析与报告接入

> Worker B note 2026-05-27: 本切片补 repo 层 M1/E1/S1 报告合同、daily JSON 可选摘要字段、周/月报模板入口和 synthetic 示例，覆盖 R21-R27 的静态文档与样例基础；不要仅凭本切片关闭 runtime/report generation 或真实 workflow wiring。

- [x] R21. 增加 M1/E1/S1 的结构化测试样例与示例输出。来源：Roadmap L121。
- [x] R22. 增加 M1/E1/S1 的结构化输出示例。来源：Roadmap L277。
- [x] R23. 将 M1/E1/S1 稳定接入周报/月报模板。来源：Roadmap L122。
- [x] R24. 将药物、运动、睡眠分析接入周报/月报。来源：Roadmap L276。
- [x] R25. 将药物/运动/睡眠分析写入可供趋势分析复用的结构化摘要。来源：Roadmap L123。
- [x] R26. 评估并扩展 `profile` 与 `goals` 模板字段：运动背景、器材、用药状态、睡眠指标等。来源：Roadmap L124。
- [x] R27. 若深度 workflow 需要更多字段，则扩展 `profile` / `goals` 模板。来源：Roadmap L278。
- [x] R28. 增加风险护栏：GLP-1、不安全运动、异常体检指标、睡眠红旗信号。来源：Roadmap L279。
- [x] R29. 将药物、体检维度在有明确来源时接入月报观察。来源：Roadmap L376。
- [ ] R30. 增加平台期检测与干预建议。来源：Roadmap L417。
- [ ] R31. 增加饮食执行度评分：热量、蛋白质、膳食纤维、连续性。来源：Roadmap L418。
- [ ] R32. 增加 GLP-1 用户肌肉流失风险评分。来源：Roadmap L420。
- [ ] R33. 增加体检指标趋势 Markdown 看板。来源：Roadmap L421。
- [ ] R34. 增加伤病感知训练进阶。来源：Roadmap L422。
- [ ] R35. 增加睡眠规律性与恢复评分。来源：Roadmap L423。

## C. Phase 4A 发布打磨

> C 组状态注记（2026-05-27）：本轮只做不需要用户测试的 release hardening，
> 包括 CHANGELOG、公开发布 checklist、隐私/医学边界和 README 发布/模型/隐私口径。
> 复选框保留原 Roadmap 映射，主线吸收时再统一决定是否关闭。

- [x] R36. 增加 `CHANGELOG.md`。来源：Roadmap L138。
- [x] R37. 增加 `CHANGELOG.md`。来源：Roadmap L235。
- [x] R38. 增加 `CHANGELOG.md`。来源：Roadmap L390。
- [x] R39. 增加公开发布 checklist。来源：Roadmap L291。
- [x] R40. 增加发布 checklist。来源：Roadmap L392。
- [x] R41. 若公开发布，运行 secret scan。来源：Roadmap L393。
- [x] R42. 做发布前检查：secret scan、ignored runtime files、文档链接、Markdown 质量。来源：Roadmap L144。
- [x] R43. 运行 Markdown 链接检查。来源：Roadmap L394。
- [x] R44. 讲清隐私与云端模型边界。来源：Roadmap L395。
- [x] R45. 讲清这不是医学诊断。来源：Roadmap L396。
- [x] R46. 让 clone + setup 路径清晰。来源：Roadmap L400。
- [x] R47. 确保 README、docs、deploy、SKILL 的运行时路径合同一致。来源：Roadmap L401。
- [x] R48. 确保公开文案与真实实现范围一致。来源：Roadmap L402。
- [x] R49. 启动 Phase 4A 发布打磨。来源：Roadmap L454。

## D. 数据与集成扩展

> 状态注记（2026-05-27）：D 组外部数据/集成扩展已暂停并延后；不得纳入本轮
> Phase 4A 公开发布能力声明。

- [ ] R50. 增加 Apple Health 原生 XML parser，用于未来历史批量导入。来源：Roadmap L408。
- [ ] R51. 增加 Health Auto Export 集成，用于未来定期导入 Apple Health CSV/JSON。来源：Roadmap L409。
- [ ] R52. 增加 Withings/体脂秤导入体重与身体成分。来源：Roadmap L410。
- [ ] R53. 增加食物照片复核模式：先估算，再请用户确认份量。来源：Roadmap L411。
- [ ] R54. 增加营养标签 OCR 置信度与纠错流程。来源：Roadmap L412。
- [ ] R55. 增加药物/补剂日程追踪。来源：Roadmap L413。

## E. 使用体验

> 状态注记（2026-05-27）：E 组 UX 扩展已暂停并延后；不得纳入本轮 Phase 4A
> 公开发布能力声明。

- [ ] R56. 增加 Telegram 快捷操作：常吃餐、体重、睡眠、运动。来源：Roadmap L427。
- [ ] R57. 增加“这周和上周比有什么变化？”命令。来源：Roadmap L428。
- [ ] R58. 增加“生成就诊摘要”命令。来源：Roadmap L429。
- [ ] R59. 增加“导出最近 30 天”命令。来源：Roadmap L430。
- [ ] R60. 增加 OCR 或热量估算错误时的友好纠正流程。来源：Roadmap L431。

## F. 可选工程化输出

> 状态注记（2026-05-27）：F 组可选 dashboard 输出已暂停并延后；不得纳入本轮
> Phase 4A 公开发布能力声明。

- [ ] R61. 可选：从 `workspace/data/` 生成静态 dashboard。来源：Roadmap L440。
