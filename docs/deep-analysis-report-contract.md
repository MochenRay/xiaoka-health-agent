# M1/E1/S1 深度分析报告合同

> 目标：定义药物、运动、睡眠深度分析如何输出结构化摘要，并如何保守接入周报和月报。本文只定义 repo 层合同，不改 OpenClaw runtime，不使用个人健康数据。

## 适用范围

本合同覆盖三个 workflow：

- `M1`：药物与补剂状态整理、GLP-1 决策支持、监测提醒。
- `E1`：运动建议、训练负荷整理、伤病感知安全边界。
- `S1`：睡眠时长、规律性、效率和恢复趋势整理。

这些 workflow 的输出是 `analysis_summaries`，用于报告复用；它们不是原始记录，不能覆盖 `nutrition`、`exercise`、`sleep`、`supplements` 等 daily JSON 原始字段。

## 通用结构化输出

M1/E1/S1 统一输出以下字段。字段可存入 `workspace/data/YYYY-MM/DD.json` 的 `analysis_summaries`，也可在报告生成过程中临时生成同形结构。

```json
{
  "workflow": "M1",
  "version": "phase3b-static-v1",
  "status": "ready",
  "period": {
    "start": "2026-07-01",
    "end": "2026-07-07"
  },
  "source_scope": [
    "workspace/data/2026-07/01.json",
    "config/profile.md",
    "config/goals.md"
  ],
  "summary": "可直接进入报告的一句话摘要。",
  "trend_inputs": {},
  "flags": [],
  "report_carry_forward": false
}
```

### 通用字段规则

| 字段 | 规则 |
|------|------|
| `workflow` | 固定为 `M1` / `E1` / `S1`。 |
| `version` | 合同或 prompt 版本；当前使用 `phase3b-static-v1`。 |
| `status` | `not_run` / `insufficient_data` / `background_only` / `ready` / `needs_review`。 |
| `period.start/end` | 摘要覆盖日期；单日摘要可两者相同。 |
| `source_scope` | 只列实际读取的 repo 路径或结构化来源，不列未读取来源。 |
| `summary` | 报告可复用摘要；必须弱断言，不诊断、不处方。 |
| `trend_inputs` | 供周/月趋势聚合的结构化指标；未知值用 `null` 或缺省，不用 `0` 代表未知。 |
| `flags` | 只放来源明确的提醒项；无提醒用空数组。 |
| `report_carry_forward` | 是否允许月报在无更新时复用；默认 `false`。 |

## M1 药物/补剂摘要

M1 只处理来源明确的信息：`config/profile.md` 的当前用药/补剂状态、`config/goals.md` 的目标、`workspace/medical/` 中明确存在的体检文件，以及用户当次明确提供的信息。

不得从体重、热量或睡眠变化反推药物效果。不得根据 profile 背景写出每日服药依从性。

### M1 `trend_inputs`

```json
{
  "medication_status": "none_recorded",
  "supplement_status": "recorded",
  "adherence_recorded": false,
  "monitoring_needed": false,
  "clinician_review_needed": false,
  "interaction_flags": []
}
```

允许值：

- `medication_status`：`none_recorded` / `considering` / `active` / `paused` / `discontinued` / `unknown`
- `supplement_status`：`none_recorded` / `recorded` / `changed` / `unknown`
- `interaction_flags[]`：只写来源明确的药物-补剂或用药边界提醒。

### M1 报告接入

周报：

- 有本周 M1 摘要时，只写状态、来源、需复核事项和边界。
- 没有 M1 摘要时，固定写：`本周没有新的 M1 结构化摘要；不做药物效果、依从性或剂量判断。`

月报：

- 有当月 M1 摘要时，可汇总状态变化和监测提醒。
- 只有 `report_carry_forward: true` 的摘要才可跨周期复用。
- 涉及药物、GLP-1、体检指标时必须写医学边界：不构成诊断、处方或自行调整剂量建议。

## E1 运动摘要

E1 读取 profile 的运动背景、器材、伤病限制和 goals 的训练目标；趋势统计优先来自 daily JSON 的 `exercise`、`activity_summary`、`steps`。

### E1 `trend_inputs`

```json
{
  "sessions": 3,
  "total_duration_min": 150,
  "total_active_energy_kcal": 960,
  "dominant_types": ["strength", "walking"],
  "equipment_used": ["dumbbell", "bodyweight"],
  "injury_constraints_respected": true,
  "progression_signal": "stable"
}
```

规则：

- 运动记录少于 3 天时，不做训练趋势判断，只做记录回顾。
- 伤病限制缺失时，不输出“安全”结论；只写“伤病背景未记录，动作安全性未评估”。
- `progression_signal` 可为 `improving` / `stable` / `decreasing` / `insufficient_data`。

### E1 报告接入

周报：

- 聚合训练次数、时长、类型、伤病边界是否有明确记录。
- 数据不足时固定写：`运动记录不足 3 天，仅保留本周记录，不做训练趋势判断。`

月报：

- 聚合周均训练频次、主要训练类型、负荷方向和下月训练重点。
- 不生成超出器材、伤病限制或可用时间的计划。

## S1 睡眠摘要

S1 优先读取 daily JSON 的 `sleep` 字段；如无 JSON，可在 runtime prompt 中从日志补结算后再分析。目标和约束来自 `config/profile.md` 与 `config/goals.md`。

### S1 `trend_inputs`

```json
{
  "sleep_days": 5,
  "avg_duration_h": 7.2,
  "target_duration_h": 7.5,
  "avg_efficiency_pct": 91,
  "regularity_signal": "stable",
  "late_sleep_days": 1,
  "recovery_signal": "mixed"
}
```

规则：

- 睡眠记录少于 3 天时，不做规律性或趋势判断。
- 缺少开始/结束时间时，不计算规律性。
- 睡眠红旗信号只能基于用户明确记录或设备字段；不诊断睡眠障碍。

### S1 报告接入

周报：

- 汇总平均时长、记录天数、是否达到目标和最明显的一个改进点。
- 数据不足时固定写：`睡眠记录不足 3 天，仅保留当前观察，不做趋势判断。`

月报：

- 汇总睡眠目标达成、规律性方向、恢复相关观察和下月重点。
- 若存在持续极低睡眠、明显白天功能受影响等明确来源提醒，只建议线下专业评估，不作诊断。

## 数据不足和边界

- 任一 workflow 没有运行或没有结构化摘要时，不从其他维度补猜。
- 有原始运动/睡眠数据但没有 E1/S1 摘要时，报告可做基础统计，但不能声称完成深度分析。
- M1 不使用 daily JSON 的 `supplements` 字段推断用药效果。
- 所有药物、体检和睡眠红旗内容都必须是提醒，不是诊断或处方。
- 不触碰、不生成、不反推个人健康数据；synthetic fixture 必须显式标记为非真实数据。
