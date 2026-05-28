# 数据 Schema 说明

## 每日数据 JSON

零点结算后生成，存放在 `workspace/data/YYYY-MM/DD.json`。
对应的源日志路径为 `workspace/logs/YYYY-MM/DD.md`。

```json
{
  "date": "2026-03-24",
  "weight": {
    "value": 104.5,
    "unit": "kg",
    "source": "manual"
  },
  "nutrition": {
    "total_calories": 1850,
    "protein_g": 135,
    "carbs_g": 180,
    "fat_g": 62,
    "meals": [
      {
        "time": "08:30",
        "type": "breakfast",
        "items": [
          {
            "name": "煮鸡蛋",
            "amount": "2个",
            "calories": 156,
            "protein": 12.6,
            "carbs": 1.2,
            "fat": 10.6
          }
        ],
        "calories": 156
      }
    ]
  },
  "exercise": {
    "total_burn": 320,
    "activities": [
      {
        "type": "swimming",
        "duration_min": 40,
        "calories": 320,
        "active_energy_kcal": 320,
        "distance_km": 1.2,
        "start_time": "19:20",
        "end_time": "20:00",
        "source": "google_health_api_healthkit",
        "source_platform": "HEALTH_KIT",
        "confidence": "high",
        "note": ""
      }
    ]
  },
  "activity_summary": {
    "active_energy_kcal": 520,
    "source": "google_health_api_healthkit",
    "source_platform": "HEALTH_KIT",
    "confidence": "medium",
    "note": ""
  },
  "steps": {
    "count": 8200,
    "source": "google_health_api_healthkit",
    "source_platform": "HEALTH_KIT"
  },
  "sleep": {
    "duration_h": 7.5,
    "source": "google_health_api_healthkit",
    "source_platform": "HEALTH_KIT",
    "start_time": "23:40",
    "end_time": "07:10",
    "time_in_bed_h": 8.0,
    "efficiency_pct": 94,
    "stages": {
      "awake_min": 20,
      "rem_min": 95,
      "core_min": 260,
      "deep_min": 75
    },
    "quality": null,
    "confidence": "medium",
    "note": ""
  },
  "supplements": ["vitamin_d_2000iu", "creatine_5g", "omega3"],
  "analysis_summaries": {
    "m1_medication": {
      "workflow": "M1",
      "version": "phase3b-static-v1",
      "status": "background_only",
      "period": {
        "start": "2026-03-24",
        "end": "2026-03-24"
      },
      "source_scope": ["config/profile.md", "config/goals.md"],
      "summary": "仅有用药/补剂背景，未做药物效果或剂量判断。",
      "trend_inputs": {
        "medication_status": "unknown",
        "supplement_status": "recorded",
        "adherence_recorded": false,
        "monitoring_needed": false,
        "clinician_review_needed": false,
        "interaction_flags": []
      },
      "flags": [],
      "report_carry_forward": false
    },
    "e1_exercise": {
      "workflow": "E1",
      "version": "phase3b-static-v1",
      "status": "ready",
      "period": {
        "start": "2026-03-24",
        "end": "2026-03-24"
      },
      "source_scope": ["workspace/data/2026-03/24.json", "config/profile.md", "config/goals.md"],
      "summary": "本日有 1 次游泳记录，未发现来源明确的伤病冲突。",
      "trend_inputs": {
        "sessions": 1,
        "total_duration_min": 40,
        "total_active_energy_kcal": 320,
        "dominant_types": ["swimming"],
        "equipment_used": [],
        "injury_constraints_respected": true,
        "progression_signal": "insufficient_data"
      },
      "flags": [],
      "report_carry_forward": false
    },
    "s1_sleep": {
      "workflow": "S1",
      "version": "phase3b-static-v1",
      "status": "ready",
      "period": {
        "start": "2026-03-24",
        "end": "2026-03-24"
      },
      "source_scope": ["workspace/data/2026-03/24.json", "config/profile.md", "config/goals.md"],
      "summary": "本日睡眠 7.5 小时，单日数据不做趋势判断。",
      "trend_inputs": {
        "sleep_days": 1,
        "avg_duration_h": 7.5,
        "target_duration_h": null,
        "avg_efficiency_pct": 94,
        "regularity_signal": "insufficient_data",
        "late_sleep_days": null,
        "recovery_signal": "insufficient_data"
      },
      "flags": [],
      "report_carry_forward": false
    }
  },
  "notes": ""
}
```

### 字段说明

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `date` | string | 是 | 格式 YYYY-MM-DD |
| `weight.value` | number | 否 | 体重（kg），当天未记录则整个 weight 为 null |
| `weight.unit` | string | 否 | 固定 "kg" |
| `weight.source` | string | 否 | "manual" / "apple_health_screenshot" / "scale_photo" |
| `nutrition.total_calories` | number | 否 | 当天总摄入热量 |
| `nutrition.protein_g` | number | 否 | 当天总蛋白质（g） |
| `nutrition.carbs_g` | number | 否 | 当天总碳水（g） |
| `nutrition.fat_g` | number | 否 | 当天总脂肪（g） |
| `nutrition.meals` | array | 否 | 每餐详细记录 |
| `nutrition.meals[].time` | string | 否 | 进食时间 HH:MM |
| `nutrition.meals[].type` | string | 否 | "breakfast" / "lunch" / "dinner" / "snack" |
| `nutrition.meals[].items` | array | 是(per meal) | 食物列表 |
| `nutrition.meals[].calories` | number | 是(per meal) | 本餐总热量 |
| `exercise.total_burn` | number | 否 | 当天总运动消耗 |
| `exercise.activities` | array | 否 | 运动详细记录 |
| `exercise.activities[].type` | string | 是(per act) | 运动类型 |
| `exercise.activities[].duration_min` | number | 否 | 时长（分钟） |
| `exercise.activities[].calories` | number | 否 | 消耗热量 |
| `exercise.activities[].active_energy_kcal` | number | 否 | 设备或截图给出的 active calories；无设备数据时可为空 |
| `exercise.activities[].source` | string | 否 | "manual" / "google_health_api" / "google_health_api_healthkit" / legacy screenshot source |
| `exercise.activities[].source_platform` | string | 否 | Google Health API 来源平台，如 "HEALTH_KIT"；不写用户 id |
| `exercise.activities[].start_time` | string | 否 | 开始时间 HH:MM，可识别或 API 可映射时填写 |
| `exercise.activities[].end_time` | string | 否 | 结束时间 HH:MM，可识别或 API 可映射时填写 |
| `exercise.activities[].distance_km` | number | 否 | 距离（km），可识别或 API 可映射时填写 |
| `exercise.activities[].steps` | number | 否 | 该次活动步数，可识别或 API 可映射时填写 |
| `exercise.activities[].confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `exercise.activities[].note` | string | 否 | 备注或用户确认信息 |
| `activity_summary.active_energy_kcal` | number | 否 | 日级 active energy；不是单次 workout |
| `activity_summary.source` | string | 否 | "manual" / "google_health_api" / "google_health_api_healthkit" / legacy screenshot source |
| `activity_summary.source_platform` | string | 否 | Google Health API 来源平台，如 "HEALTH_KIT"；不写用户 id |
| `activity_summary.confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `activity_summary.note` | string | 否 | 备注或用户确认信息 |
| `steps.count` | number | 否 | 当日步数；未记录则 steps 可为空 |
| `steps.source` | string | 否 | "manual" / "google_health_api" / "google_health_api_healthkit" / legacy screenshot source |
| `steps.source_platform` | string | 否 | Google Health API 来源平台，如 "HEALTH_KIT"；不写用户 id |
| `sleep.duration_h` | number | 否 | 睡眠时长（小时） |
| `sleep.source` | string | 否 | "manual" / "google_health_api" / "google_health_api_healthkit" / legacy screenshot source |
| `sleep.source_platform` | string | 否 | Google Health API 来源平台，如 "HEALTH_KIT"；不写用户 id |
| `sleep.start_time` | string | 否 | 睡眠开始时间 HH:MM，可识别或 API 可映射时填写 |
| `sleep.end_time` | string | 否 | 睡眠结束时间 HH:MM，可识别或 API 可映射时填写 |
| `sleep.time_in_bed_h` | number | 否 | 卧床时间（小时），可识别或 API 可映射时填写 |
| `sleep.efficiency_pct` | number | 否 | 睡眠效率百分比，可识别或 API 可映射时填写 |
| `sleep.stages.awake_min` | number | 否 | 清醒分钟数 |
| `sleep.stages.rem_min` | number | 否 | REM 睡眠分钟数 |
| `sleep.stages.core_min` | number | 否 | 核心睡眠分钟数 |
| `sleep.stages.deep_min` | number | 否 | 深睡分钟数 |
| `sleep.quality` | string | 否 | "good" / "fair" / "poor" / null |
| `sleep.confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `sleep.note` | string | 否 | 备注或用户确认信息 |
| `supplements` | array | 否 | 补剂列表（格式：名称_剂量） |
| `analysis_summaries` | object | 否 | M1/E1/S1 深度分析结构化摘要；可缺省 |
| `analysis_summaries.m1_medication` | object | 否 | 药物/补剂摘要；只记录来源明确的状态、提醒和报告摘要 |
| `analysis_summaries.e1_exercise` | object | 否 | 运动深度摘要；可复用训练次数、时长、伤病边界等趋势输入 |
| `analysis_summaries.s1_sleep` | object | 否 | 睡眠深度摘要；可复用睡眠天数、均值、效率、规律性等趋势输入 |
| `analysis_summaries.*.workflow` | string | 是(when present) | "M1" / "E1" / "S1" |
| `analysis_summaries.*.version` | string | 是(when present) | 合同或 prompt 版本，当前为 "phase3b-static-v1" |
| `analysis_summaries.*.status` | string | 是(when present) | "not_run" / "insufficient_data" / "background_only" / "ready" / "needs_review" |
| `analysis_summaries.*.period` | object | 否 | 摘要覆盖日期，包含 `start` / `end` |
| `analysis_summaries.*.source_scope` | array | 否 | 实际读取的来源路径或结构化来源；不得列未读取来源 |
| `analysis_summaries.*.summary` | string | 否 | 可进入周报/月报的一句话摘要；必须弱断言 |
| `analysis_summaries.*.trend_inputs` | object | 否 | 供趋势聚合复用的结构化指标；未知值用 null 或缺省 |
| `analysis_summaries.*.flags` | array | 否 | 来源明确的安全提醒；无则为空数组 |
| `analysis_summaries.*.report_carry_forward` | boolean | 否 | 是否允许后续报告在无更新时复用该摘要；默认 false |
| `notes` | string | 否 | 备注 |

### 深度分析摘要约定

- `analysis_summaries` 只保存 M1/E1/S1 的结构化摘要，不保存原始对话，不替代 daily JSON 原始字段。
- M1 不得从体重、热量或睡眠变化反推药物效果；若没有明确每日用药记录，`adherence_recorded` 必须为 `false` 或缺省。
- E1 可复用 `exercise`、`activity_summary`、`steps` 作为训练趋势输入；运动记录少于 3 天时，`progression_signal` 应为 `insufficient_data`。
- S1 可复用 `sleep` 字段做趋势输入；睡眠记录少于 3 天时，`regularity_signal` 应为 `insufficient_data`。
- 药物、体检、睡眠红旗内容只能作为提醒，不构成诊断、处方或自行调整剂量建议。
- 详细报告合同见 `docs/deep-analysis-report-contract.md`。

### Google Health API 优先字段约定

- Google Health API 是 Apple Health / HealthKit 运动、步数、睡眠数据的主接入路径；截图仅作为 fallback。
- `steps` 优先使用 `dataTypes/steps/dataPoints:dailyRollUp` 生成日级 count；原始 data points 可用于排查，但不应长期保存完整响应。
- `sleep` 与 `exercise` 先按日期窗口读取 data points，再规范化到当日日志或 daily JSON。
- `exercise.activities[]` 只记录单次 workout；活动/步数/消耗摘要写入 `activity_summary` 与 `steps`，不要伪装成单次运动。
- daily JSON 可保存 `source_platform`、`source_application`、`source_device_form_factor` 等非敏感来源字段；不得保存 token、账号 email、`healthUserId`、`legacyUserId` 或完整原始响应。
- 日级可选对象如 `nutrition`、`exercise`、`activity_summary`、`steps`、`sleep` 可缺省或为 `null`；不要用 `0` 代表未知。
- Google Health API 接入细节见 `docs/google-health-api-ingestion.md`。

### 截图 fallback 字段约定

- Apple Watch / Apple Health 截图字段都是可选 fallback 字段，不要求历史批量导入。
- 运动截图必须能识别日期、运动类型、时长、active calories 和来源；活动摘要截图必须能识别日期、steps 或 active calories、来源；睡眠截图必须能识别日期、睡眠时长和来源。
- 若必填识别项缺失或 `confidence` 为 `low`，Agent 应先向用户确认，不应自行补全。
- Synthetic screenshot fixture 位于 `fixtures/synthetic/phase2c/`，只验证已确认识别结果到 Markdown 与 expected JSON 的字段映射，不验证 OCR 质量或 runtime 结算。
- 本 schema 不定义 Apple Health XML、Health Auto Export CSV/JSON 或 parser staging schema；未来如做文件式批量导入再单独扩展。

## 自建食物库 JSON

存放在 `workspace/food-library/my-foods.json`。

```json
[
  {
    "name": "优形即食鸡胸肉（原味）",
    "brand": "优形",
    "per_100g": {
      "calories": 110,
      "protein": 22,
      "carbs": 2.5,
      "fat": 1.8
    },
    "common_serving": {
      "amount": "1袋(100g)",
      "calories": 110
    },
    "source": "nutrition_label_photo",
    "added_date": "2026-03-24"
  }
]
```

### 字段说明

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 食物名称 |
| `brand` | string | 否 | 品牌 |
| `per_100g.calories` | number | 是 | 每 100g 热量 |
| `per_100g.protein` | number | 是 | 每 100g 蛋白质（g） |
| `per_100g.carbs` | number | 是 | 每 100g 碳水（g） |
| `per_100g.fat` | number | 是 | 每 100g 脂肪（g） |
| `common_serving` | object | 否 | 常见份量 |
| `source` | string | 否 | "nutrition_label_photo" / "manual" / "brand_website" |
| `added_date` | string | 否 | 添加日期 |
