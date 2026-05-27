# Privacy and Medical Boundaries

本文件定义 Xiaoka 公开发布时必须讲清的隐私、云端模型、医学边界和 screenshot/OCR
限制。README、发布页和模板说明不得弱化这些边界。

## Local storage boundary

- Xiaoka 默认把用户健康资料保存在本地仓库的 `config/` 和 `workspace/` 下。
- `config/profile.md`、`config/goals.md` 和 `workspace/*` 默认被 `.gitignore`
  忽略，不应进入公开 commit。
- `workspace/README.md` 和 `fixtures/synthetic/` 可以被 tracked，但只能包含说明或
  synthetic 非私人样例。
- 仓库不会主动提供远端数据库或自有服务器同步；是否同步到第三方取决于用户部署的
  AI 平台、Git 客户端、备份工具和云盘设置。
- 发布、提交或导出前，用户应先运行 secret scan 与 ignored runtime files 检查。

## Cloud model caveat

- Xiaoka 支持多模型部署；具体模型由 OpenClaw、Claude Code、API gateway 或其他运行
  环境绑定。
- 使用云端模型 API 时，对话内容、用户输入、截图、图片、OCR 结果和必要健康上下文可能会
  发送给模型提供商处理。
- 如果用户需要完全离线运行，应选择本地模型和本地推理环境；但截图、照片、营养标签和
  体检单图片工作流仍要求本地模型具备图片输入、图片识别或 OCR 能力。
- 模型选择只影响理解质量、OCR/Vision 质量和遵循指令的稳定性，不改变 Xiaoka 的
  `config/` 与 `workspace/` 路径合同。
- 不应在公开文档中把某个固定云模型写成长期推荐；发布前应按当前部署环境重新核验。

## Medical boundary

- Xiaoka 是健康记录、整理和决策支持工具，不是医生、医疗器械或诊疗系统。
- Xiaoka 不提供医疗诊断、处方、药物剂量调整、急症分诊或替代医生的治疗建议。
- 体检指标、GLP-1、补剂、运动和睡眠分析只能输出信息整理、风险提醒、可讨论的问题和
  就医沟通建议。
- 出现胸痛、呼吸困难、意识障碍、严重过敏、严重低血糖、极端异常化验值或其他紧急情况时，
  用户应立即联系当地急救或专业医疗服务。
- 对药物、补剂、训练计划或饮食方案的实际调整，应由用户和合格医疗专业人士共同决定。

## Screenshot and OCR limitations

- Apple Watch / Apple Health 截图、食物照片、营养标签和体检单图片必须由具备图片识别或
  OCR 能力的多模态模型处理。
- Text-only 模型可以继续支持文字记录、报告整理和健康问答，但不能可靠读取图片；遇到截图
  时必须要求用户手动转写关键字段。
- OCR 可能误读日期、单位、时长、active calories、睡眠时长、检验项目名或参考范围。
- 图片裁切、低分辨率、遮挡、语言混排、界面版本变化和单位差异都会降低识别可靠性。
- Phase 2C synthetic fixture 只验证“已确认识别结果 -> Markdown 日志 -> expected
  daily JSON”的映射，不验证真实 OCR 质量、图片渲染或 OpenClaw runtime。
- 当关键字段缺失或置信度不足时，Xiaoka 应追问或要求用户确认，不得编造缺失值。

## Public wording guardrails

- 可以说：本地文件驱动、路径合同稳定、synthetic fixture validators 已覆盖截图 mapping
  与 C8 静态合同。
- 不可说：真实截图/OCR、C8 runtime 周/月报、Apple Health 历史同步或医学趋势分析已经
  完整闭环，除非对应 runtime smoke 已完成并登记。
- 所有公开能力声明应能追溯到 README、`CHANGELOG.md`、release checklist 或对应 validator。
