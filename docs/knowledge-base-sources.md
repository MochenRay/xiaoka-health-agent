# 知识库数据来源与验证记录

> 完整验证报告见 `PRD.md` 附录 A。

## 来源总览

| 文件 | 主要数据源 | 最近验证 | 精度说明 |
|------|-----------|---------|---------|
| nutrition.md | Mifflin-St Jeor, 中国居民膳食指南 | 2026-03-24 | 活动因子±15% |
| medical-markers.md | 临床医学指南 | 2026-03-24 | 参考范围因实验室而异 |
| medications.md | NEJM (STEP/SURMOUNT), Lilly, PMC | 2026-03-24 | 价格可能过时 |
| supplements.md | WebMD, Harvard Health, PubMed | 2026-03-24 | 剂量为一般成人推荐 |
| exercise.md | ACSM, NSCA 运动科学指南 | 2026-03-24 | 热量消耗±20% |
| wearables.md | 厂商官方数据 | 2026-03-24 | 价格/功能可能随产品更新变化 |
| cn-brands.md | AI 估算（未逐条实测） | 2026-03-24 | 部分偏差较大，以包装标注为准 |
| cn-food-db.json | 中国食物成分表标准版第 6 版 | 2026-03-24 | 权威数据，1,677 条基础食材 |

## 已验证数据点

### medications.md
- STEP 1 semaglutide -14.9% → ✅ NEJM 确认
- SURMOUNT-1 tirzepatide -22.5% → ✅ 已修正（原数据 -20.9%）
- 停药反弹 2/3 → ✅ PMC 确认
- 恶心率 44% → ✅ STEP 1-3 确认

### nutrition.md
- 男性 BMR 公式 → ✅ 已修正（原数据混入女性常数 -161）
- 蛋白质每餐上限 40-50g → ✅ PMC 确认
- 活动因子 1.2-1.9 → ✅ 业界标准

### supplements.md
- 肌酸 3-5g/天 → ✅ WebMD/Harvard 确认
- 褪黑素 0.5-3mg → ✅ Sleep Foundation 确认
- 铁+钙分开服用 → ✅ PubMed 确认

### cn-brands.md（抽查 3 个点）
- 霸王茶姬伯牙绝弦 ~400kcal → 实际约 290kcal（偏高 38%）
- 瑞幸生椰拿铁 ~260kcal → 实际 149-185kcal（偏高 40-75%）
- 山姆麻薯面包 ~180kcal → 实际约 218kcal（偏低 17%）
