# Xiaoka Health Agent PRD

> 最近更新：2026-05-28 CST
> 本文件是当前仓库的 PRD 索引与范围合同。旧 PRD 来源为
> `/Users/rayli/health-coach/docs/PRD-xiaoka-health-agent.md`；若旧 PRD
> 与本仓库现有文档冲突，以本文件和本仓库当前合同为准。

## 产品定位

小卡是本地文件驱动的 AI 健康教练 Agent 包。它不做后端服务，也不替代
Apple Health、薄荷健康、医院系统或医生；它负责把健康档案、饮食、体重、
运动、睡眠、补剂和体检记录整理到本地 `config/` 与 `workspace/`，并用
AI 做结构化记录、解释和低断言强度分析。

## 当前阶段合同

| 阶段 | 当前合同 | 状态 |
|------|----------|------|
| Phase 1 最小可用 | [phase1-minimum-contract.md](phase1-minimum-contract.md) | 已完成 |
| Phase 2A OpenClaw runtime 规格 | [openclaw-runtime.md](openclaw-runtime.md) | 已完成 |
| Phase 2B 周报/月报自动化 | [report-automation.md](report-automation.md) | 已完成，已做零覆盖与 synthetic 非零 runtime 验证 |
| Phase 2C 设备数据接入 | [google-health-api-ingestion.md](google-health-api-ingestion.md)、[data-schema.md](data-schema.md) 与 `fixtures/synthetic/phase2c/` | Google Health API read smoke 已通过；截图路径降级为 fallback；正式 importer/runtime 未完成 |
| Phase 3A C8 跨维度洞察 | [c8-cross-dimensional-insights.md](c8-cross-dimensional-insights.md) | 静态合同与 fixtures 已完成；runtime smoke 未完成 |
| Phase 4A 公开发布打磨 | [../plans/phase4a-readiness-assessment.md](../plans/phase4a-readiness-assessment.md) | 待启动 |

项目路线图与完成情况见
[xiaoka-project-roadmap-checklist.md](../plans/xiaoka-project-roadmap-checklist.md)。

## 当前明确不做

- 不做食品条码扫描。
- 不做实时运动追踪。
- 不做医疗诊断、处方或药物调整。
- 当前还没有把 Google Health API 接入为正式自动同步器。
- 当前不做 Apple Health 文件式历史批量导入。
- 当前不做 Health Auto Export 自动同步。
- 当前不做 Apple Health 原生 XML parser。
- 数据不足时不硬编趋势、因果或跨维度结论。

## 公开表述边界

- 可说：小卡是本地文件驱动的健康 Agent 包，核心 workflow、OpenClaw 五条
  cron、周报/月报、Google Health API read smoke、截图 fallback mapping fixture、C8 静态合同均已建立。
- 不可说：Google Health API 自动同步、真实 OCR、Apple Health 文件式历史同步、C8 runtime 报告、医学趋势分析
  已完整闭环，除非对应 runtime smoke 已完成并登记。
- 公开 README、发布页和简历材料必须区分 `static fixture validation` 与
  `OpenClaw runtime validation`。
