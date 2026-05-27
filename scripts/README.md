# Scripts

此目录用于 Phase 2 之后的辅助脚本。

当前仓库的 Phase 1 最小可用不依赖任何脚本，重点是：

- `agent.md` 和 `SKILL.md` 的行为约束
- `references/` 知识库
- `config/`、`templates/`、`workspace/` 的运行时约定

当前已有脚本：

- `validate_daily_json_schema.py`：校验 `fixtures/synthetic/**/workspace/data/`
  下的非私人 daily JSON fixture；覆盖日期格式、顶层可选对象/null 字段、
  关键数值字段、M1/E1/S1 `analysis_summaries` 合同、synthetic 标记和常见真实个人标识防护。
- `validate_phase2b_fixtures.py`：校验 Phase 2B synthetic 周报/月报 fixtures。
- `validate_phase2c_screenshot_fixtures.py`：校验 Phase 2C screenshot-first
  synthetic fixtures，覆盖已确认截图识别结果到 Markdown 日志和 expected
  daily JSON 的字段映射；不验证 OCR 或 runtime 结算。
- `validate_phase3a_c8_fixtures.py`：校验 Phase 3A C8 synthetic fixture
  shape、expected report 的 `## 跨维度观察` section wording，以及 selected
  source-backed metrics。
- `validate_report_contracts.py`：校验 `docs/report-automation.md`、
  `docs/c8-cross-dimensional-insights.md`、`docs/deep-analysis-report-contract.md`、
  周/月报模板和 Phase 3B expected report sections 中的标准 runtime 路径、
  `NO_REPLY`、C8 / M1 / E1 / S1 section 结构，以及旧根目录 runtime 路径是否只出现在禁止/兼容语境。
- `validate_settlement_prompt_contract.py`：校验 synthetic 每日日志到 expected
  daily JSON 的结算 prompt 回归合同；只验证 repo 层 prompt/spec 与 fixture，
  不运行 OpenClaw cron。
- `validate_repository_contract.py`：校验仓库级轻量合同，包括 Markdown 本地链接、
  tracked JSON 合法性、`references/*.md` metadata、`SKILL.md` 行数，以及旧根目录
  runtime 路径只出现在兼容/禁止语境中。

后续可能放入这里的脚本包括：

- Apple Health 导出解析（未来可选方向；当前 Phase 2C 不实现）
- 历史数据迁移
- JSON 结算校验辅助工具
