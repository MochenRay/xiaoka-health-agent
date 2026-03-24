# 数据 Schema 说明

## 每日数据 JSON

零点结算后生成，存放在 `workspace/data/YYYY-MM/DD.json`。

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
        "source": "apple_health_screenshot"
      }
    ]
  },
  "sleep": {
    "duration_h": 7.5,
    "quality": null
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
| `exercise.activities[].source` | string | 否 | 数据来源 |
| `sleep.duration_h` | number | 否 | 睡眠时长（小时） |
| `sleep.quality` | string | 否 | "good" / "fair" / "poor" / null |
| `supplements` | array | 否 | 补剂列表（格式：名称_剂量） |
| `notes` | string | 否 | 备注 |

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
