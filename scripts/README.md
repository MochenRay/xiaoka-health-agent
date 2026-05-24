# Scripts

此目录用于 Phase 2 之后的辅助脚本。

当前仓库的 Phase 1 最小可用不依赖任何脚本，重点是：

- `agent.md` 和 `SKILL.md` 的行为约束
- `references/` 知识库
- `config/`、`templates/`、`workspace/` 的运行时约定

当前已有脚本：

- `validate_phase2b_fixtures.py`：校验 Phase 2B synthetic 周报/月报 fixtures。
- `validate_phase2c_screenshot_fixtures.py`：校验 Phase 2C screenshot-first
  synthetic fixtures，覆盖已确认截图识别结果到 Markdown 日志和 expected
  daily JSON 的字段映射；不验证 OCR 或 runtime 结算。
- `validate_phase3a_c8_fixtures.py`：校验 Phase 3A C8 synthetic fixture
  shape、expected report 的 `## 跨维度观察` section wording，以及 selected
  source-backed metrics。

后续可能放入这里的脚本包括：

- Apple Health 导出解析（未来可选方向；当前 Phase 2C 不实现）
- 历史数据迁移
- JSON 结算校验辅助工具
