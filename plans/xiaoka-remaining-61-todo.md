# 小卡剩余 61 项依赖待办清单

> 生成基线：2026-05-27 CST，`main` / `f430ee0`
> 来源：`plans/xiaoka-project-roadmap-checklist.md` 中全部未勾选项，共 61 项。
> 说明：本清单保留 Roadmap 的 61 个未完成映射；若多项同义或重复，实施时可用同一个切片同时关闭多处来源。

## 依赖顺序

1. 先补 runtime smoke 与可回归测试底座。
2. 再接深度分析能力，因为 M1/E1/S1、C8 runtime 都依赖稳定 daily JSON、报告 prompt 和样例。
3. 再做 Phase 4A 发布打磨，避免公开文案超过真实实现。
4. 最后推进数据集成、体验命令和可视化扩展。

## A. Runtime Smoke 与测试底座

- [ ] R01. 完成真实截图/OCR runtime 验证，并补更完整回归 fixtures。来源：Roadmap L59。
- [ ] R02. 执行“真实截图/OCR runtime smoke”这个当前最佳下一步。来源：Roadmap L452。
- [ ] R03. 积累或构造足够运动/睡眠结构化 JSON，作为趋势自动化输入。来源：Roadmap L181。
- [ ] R04. 增加非私人路径下的样例数据。来源：Roadmap L289。
- [ ] R05. 增加测试样例，让结算/报告 prompt 可安全迭代。来源：Roadmap L182。
- [ ] R06. 增加结算 JSON 的 prompt 回归测试。来源：Roadmap L438。
- [ ] R07. 增加 JSON schema validation。来源：Roadmap L439。
- [ ] R08. 增加 Mac Mini OpenClaw runtime smoke test 脚本。来源：Roadmap L435。
- [ ] R09. 增加 Mac Mini OpenClaw pull 后的人工验收 checklist。来源：Roadmap L290。
- [ ] R10. 明确模型选择只影响 OCR/Vision 质量，不改变仓库路径合同。来源：Roadmap L188。
- [ ] R11. 重新核验模型推荐区，尤其多模态能力；当前 runtime 模型为 `openai/gpt-5.4`。来源：Roadmap L237。
- [ ] R12. 公开发布前重新核验当前模型推荐。来源：Roadmap L142。
- [ ] R13. 重新验证跨维度洞察 runtime，包括真实截图/OCR runtime smoke、C8 runtime smoke 和长期趋势。来源：Roadmap L61。
- [ ] R14. 执行“C8 runtime smoke”这个当前最佳下一步。来源：Roadmap L453。
- [ ] R15. 完成真实 runtime C8 验证。来源：Roadmap L377。
- [ ] R16. 用 C8 runtime smoke 验证报告模板达到 runtime-proven。来源：Roadmap L179。
- [ ] R17. 验证真实 runtime 中有足够数据时，周报/月报包含有用跨维度分析。来源：Roadmap L383。
- [ ] R18. 验证真实 runtime 中覆盖率太低时，Agent 不做趋势断言。来源：Roadmap L384。
- [ ] R19. 补更多个人基线数据以提升建议质量。来源：Roadmap L186。
- [ ] R20. 补更多自建食物库数据以提升饮食精度。来源：Roadmap L187。

## B. 深度分析与报告接入

- [ ] R21. 增加 M1/E1/S1 的结构化测试样例与示例输出。来源：Roadmap L121。
- [ ] R22. 增加 M1/E1/S1 的结构化输出示例。来源：Roadmap L277。
- [ ] R23. 将 M1/E1/S1 稳定接入周报/月报模板。来源：Roadmap L122。
- [ ] R24. 将药物、运动、睡眠分析接入周报/月报。来源：Roadmap L276。
- [ ] R25. 将药物/运动/睡眠分析写入可供趋势分析复用的结构化摘要。来源：Roadmap L123。
- [ ] R26. 评估并扩展 `profile` 与 `goals` 模板字段：运动背景、器材、用药状态、睡眠指标等。来源：Roadmap L124。
- [ ] R27. 若深度 workflow 需要更多字段，则扩展 `profile` / `goals` 模板。来源：Roadmap L278。
- [ ] R28. 增加风险护栏：GLP-1、不安全运动、异常体检指标、睡眠红旗信号。来源：Roadmap L279。
- [ ] R29. 将药物、体检维度在有明确来源时接入月报观察。来源：Roadmap L376。
- [ ] R30. 增加平台期检测与干预建议。来源：Roadmap L417。
- [ ] R31. 增加饮食执行度评分：热量、蛋白质、膳食纤维、连续性。来源：Roadmap L418。
- [ ] R32. 增加 GLP-1 用户肌肉流失风险评分。来源：Roadmap L420。
- [ ] R33. 增加体检指标趋势 Markdown 看板。来源：Roadmap L421。
- [ ] R34. 增加伤病感知训练进阶。来源：Roadmap L422。
- [ ] R35. 增加睡眠规律性与恢复评分。来源：Roadmap L423。

## C. Phase 4A 发布打磨

- [ ] R36. 增加 `CHANGELOG.md`。来源：Roadmap L138。
- [ ] R37. 增加 `CHANGELOG.md`。来源：Roadmap L235。
- [ ] R38. 增加 `CHANGELOG.md`。来源：Roadmap L390。
- [ ] R39. 增加公开发布 checklist。来源：Roadmap L291。
- [ ] R40. 增加发布 checklist。来源：Roadmap L392。
- [ ] R41. 若公开发布，运行 secret scan。来源：Roadmap L393。
- [ ] R42. 做发布前检查：secret scan、ignored runtime files、文档链接、Markdown 质量。来源：Roadmap L144。
- [ ] R43. 运行 Markdown 链接检查。来源：Roadmap L394。
- [ ] R44. 讲清隐私与云端模型边界。来源：Roadmap L395。
- [ ] R45. 讲清这不是医学诊断。来源：Roadmap L396。
- [ ] R46. 让 clone + setup 路径清晰。来源：Roadmap L400。
- [ ] R47. 确保 README、docs、deploy、SKILL 的运行时路径合同一致。来源：Roadmap L401。
- [ ] R48. 确保公开文案与真实实现范围一致。来源：Roadmap L402。
- [ ] R49. 启动 Phase 4A 发布打磨。来源：Roadmap L454。

## D. 数据与集成扩展

- [ ] R50. 增加 Apple Health 原生 XML parser，用于未来历史批量导入。来源：Roadmap L408。
- [ ] R51. 增加 Health Auto Export 集成，用于未来定期导入 Apple Health CSV/JSON。来源：Roadmap L409。
- [ ] R52. 增加 Withings/体脂秤导入体重与身体成分。来源：Roadmap L410。
- [ ] R53. 增加食物照片复核模式：先估算，再请用户确认份量。来源：Roadmap L411。
- [ ] R54. 增加营养标签 OCR 置信度与纠错流程。来源：Roadmap L412。
- [ ] R55. 增加药物/补剂日程追踪。来源：Roadmap L413。

## E. 使用体验

- [ ] R56. 增加 Telegram 快捷操作：常吃餐、体重、睡眠、运动。来源：Roadmap L427。
- [ ] R57. 增加“这周和上周比有什么变化？”命令。来源：Roadmap L428。
- [ ] R58. 增加“生成就诊摘要”命令。来源：Roadmap L429。
- [ ] R59. 增加“导出最近 30 天”命令。来源：Roadmap L430。
- [ ] R60. 增加 OCR 或热量估算错误时的友好纠正流程。来源：Roadmap L431。

## F. 可选工程化输出

- [ ] R61. 可选：从 `workspace/data/` 生成静态 dashboard。来源：Roadmap L440。
