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
        "source": "apple_watch_workout_screenshot",
        "confidence": "high",
        "note": ""
      }
    ]
  },
  "activity_summary": {
    "active_energy_kcal": 520,
    "source": "apple_health_activity_screenshot",
    "confidence": "medium",
    "note": ""
  },
  "steps": {
    "count": 8200,
    "source": "apple_health_activity_screenshot"
  },
  "sleep": {
    "duration_h": 7.5,
    "source": "apple_health_sleep_screenshot",
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
| `exercise.activities[].active_energy_kcal` | number | 否 | 截图识别出的 active calories；无设备数据时可为空 |
| `exercise.activities[].source` | string | 否 | "manual" / "apple_watch_workout_screenshot" / "apple_health_workout_screenshot" |
| `exercise.activities[].start_time` | string | 否 | 开始时间 HH:MM，截图可识别时填写 |
| `exercise.activities[].end_time` | string | 否 | 结束时间 HH:MM，截图可识别时填写 |
| `exercise.activities[].distance_km` | number | 否 | 距离（km），截图可识别时填写 |
| `exercise.activities[].steps` | number | 否 | 该次活动步数，截图可识别时填写 |
| `exercise.activities[].confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `exercise.activities[].note` | string | 否 | 备注或用户确认信息 |
| `activity_summary.active_energy_kcal` | number | 否 | 活动摘要截图里的日级 active energy；不是单次 workout |
| `activity_summary.source` | string | 否 | "apple_health_activity_screenshot" / "apple_watch_activity_screenshot" / "manual" |
| `activity_summary.confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `activity_summary.note` | string | 否 | 备注或用户确认信息 |
| `steps.count` | number | 否 | 当日步数；未记录则 steps 可为空 |
| `steps.source` | string | 否 | "manual" / "apple_health_activity_screenshot" / "apple_watch_activity_screenshot" |
| `sleep.duration_h` | number | 否 | 睡眠时长（小时） |
| `sleep.source` | string | 否 | "manual" / "apple_watch_sleep_screenshot" / "apple_health_sleep_screenshot" |
| `sleep.start_time` | string | 否 | 睡眠开始时间 HH:MM，截图可识别时填写 |
| `sleep.end_time` | string | 否 | 睡眠结束时间 HH:MM，截图可识别时填写 |
| `sleep.time_in_bed_h` | number | 否 | 卧床时间（小时），截图可识别时填写 |
| `sleep.efficiency_pct` | number | 否 | 睡眠效率百分比，截图可识别时填写 |
| `sleep.stages.awake_min` | number | 否 | 清醒分钟数 |
| `sleep.stages.rem_min` | number | 否 | REM 睡眠分钟数 |
| `sleep.stages.core_min` | number | 否 | 核心睡眠分钟数 |
| `sleep.stages.deep_min` | number | 否 | 深睡分钟数 |
| `sleep.quality` | string | 否 | "good" / "fair" / "poor" / null |
| `sleep.confidence` | string | 否 | "high" / "medium" / "low"；低置信度应先询问确认 |
| `sleep.note` | string | 否 | 备注或用户确认信息 |
| `supplements` | array | 否 | 补剂列表（格式：名称_剂量） |
| `notes` | string | 否 | 备注 |

### 截图优先字段约定

- Apple Watch / Apple Health 截图字段都是可选增强字段，不要求历史批量导入。
- `exercise.activities[]` 只记录单次 workout；活动/步数/消耗摘要截图写入 `activity_summary` 与 `steps`，不要伪装成单次运动。
- 运动截图必须能识别日期、运动类型、时长、active calories 和来源；活动摘要截图必须能识别日期、steps 或 active calories、来源；睡眠截图必须能识别日期、睡眠时长和来源。
- 若必填识别项缺失或 `confidence` 为 `low`，Agent 应先向用户确认，不应自行补全。
- 日级可选对象如 `nutrition`、`exercise`、`activity_summary`、`steps`、`sleep` 可缺省或为 `null`；不要用 `0` 代表未知。
- Synthetic screenshot-first fixture 位于 `fixtures/synthetic/phase2c/`，只验证已确认识别结果到 Markdown 与 expected JSON 的字段映射，不验证 OCR 质量或 runtime 结算。
- 本 schema 不定义 XML、CSV 或 parser staging schema；未来如做批量导入再单独扩展。

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
