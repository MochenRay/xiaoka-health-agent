# 报告自动化规格

> 目标：让周报/月报从 `workspace/data/` 的每日 JSON 可重复生成，并能安全落入 OpenClaw Cron。

## 总原则

- 报告只读标准运行时路径，不读旧根目录 `logs/`、`data/`、`reports/`。
- 报告必须写入 `workspace/reports/`。
- 同一报告路径可重复生成；重复运行时覆盖同名文件，内容由输入数据决定。
- 覆盖率必须显式写入报告，不得在数据不足时硬做趋势判断。
- 涉及健康建议时遵守 `agent.md` 医学边界，不做诊断或处方。

## 调度建议

| 报告 | Cron | 统计区间 | 输出路径 |
|------|------|----------|----------|
| 周报 | `30 8 * * 1 @ Asia/Shanghai` | 上一个完整自然周，周一到周日 | `workspace/reports/weekly-YYYY-MM-DD.md`，其中日期为周日 |
| 月报 | `30 8 1 * * @ Asia/Shanghai` | 上一个完整自然月 | `workspace/reports/monthly-YYYY-MM.md` |

原因：每日 JSON 在次日零点后生成。周一早上跑上周、每月 1 日早上跑上月，可以避开未结算的当天数据。

## 数据准备

生成报告前先列出目标区间的每一天：

1. 若 `workspace/data/{YYYY-MM}/{DD}.json` 存在，读取该 JSON。
2. 若 JSON 缺失但 `workspace/logs/{YYYY-MM}/{DD}.md` 存在且有用户记录，先按 `docs/data-schema.md` 补结算为 JSON，再纳入报告。
3. 若 Markdown 也不存在或无用户记录，计为缺失日。
4. 补结算只能写入 `workspace/data/{YYYY-MM}/{DD}.json`，不得写旧路径。

## 覆盖率与趋势规则

- 周报覆盖率：`有 JSON 的天数 / 7`。
- 月报覆盖率：`有 JSON 的天数 / 当月天数`。
- 覆盖率为 `0` 时仍必须写入 `0/N` 报告文件，但 Telegram 输出必须为 `NO_REPLY`。
- 有效天数少于 `3` 天时，只做轻量回顾，不做趋势判断。
- 若要和上期对比，上期有效天数也必须不少于 `3` 天。
- 缺失维度不补猜；报告中写“未记录”或跳过该维度。

## 周报 Prompt 合同

OpenClaw 周报任务应使用如下语义：

```text
你是小卡的周报任务。请严格按仓库报告自动化规格执行，路径相对当前 workspace 根目录。

目标区间：使用 Asia/Shanghai 时区，统计上一个完整自然周（周一到周日）。输出文件为 `workspace/reports/weekly-{周日日期}.md`。

步骤：
1. 读取 `config/profile.md`、`config/goals.md`；缺失时继续生成报告，但标注目标值不可用。
2. 列出目标周 7 天日期。
3. 对每一天按顺序读取 `workspace/data/{YYYY-MM}/{DD}.json`；若 JSON 缺失但 `workspace/logs/{YYYY-MM}/{DD}.md` 有用户记录，先按 `docs/data-schema.md` 补结算 JSON。
4. 计算覆盖率 `X/7`，汇总体重、热量、蛋白质、运动、睡眠、补剂与备注。
5. 有效天数少于 3 天时，只做轻量回顾，不做趋势判断。
6. 按 `templates/weekly-report.md` 生成报告，写入目标路径；若文件已存在则覆盖。
7. 禁止读写旧版根目录 `logs/`、`data/`、`medical/`、`reports/`、`food-library/`。

输出要求：覆盖率为 0 时只输出 `NO_REPLY`；否则输出 3 行以内摘要和报告路径。
```

## 月报 Prompt 合同

OpenClaw 月报任务应使用如下语义：

```text
你是小卡的月报任务。请严格按仓库报告自动化规格执行，路径相对当前 workspace 根目录。

目标区间：使用 Asia/Shanghai 时区，统计上一个完整自然月。输出文件为 `workspace/reports/monthly-{YYYY-MM}.md`。

步骤：
1. 读取 `config/profile.md`、`config/goals.md`；缺失时继续生成报告，但标注目标值不可用。
2. 列出目标月全部日期。
3. 对每一天按顺序读取 `workspace/data/{YYYY-MM}/{DD}.json`；若 JSON 缺失但 `workspace/logs/{YYYY-MM}/{DD}.md` 有用户记录，先按 `docs/data-schema.md` 补结算 JSON。
4. 计算覆盖率 `X/N`，汇总体重、热量、蛋白质、运动、睡眠、补剂与备注。
5. 有效天数少于 3 天时，只做轻量回顾，不做趋势判断。
6. 如上月有效天数不少于 3 天，可做月环比；否则跳过环比。
7. 按 `templates/monthly-report.md` 生成报告，写入目标路径；若文件已存在则覆盖。
8. 禁止读写旧版根目录 `logs/`、`data/`、`medical/`、`reports/`、`food-library/`。

输出要求：覆盖率为 0 时只输出 `NO_REPLY`；否则输出 3 行以内摘要和报告路径。
```

## 下一步 Runtime 落地

创建 OpenClaw Cron 前，先按 `docs/openclaw-runtime.md` 备份 `jobs.json`，再创建周报与月报任务。验证时必须覆盖两类场景：

- 无数据：写入或覆盖 `0/N` 报告，Telegram 输出 `NO_REPLY`。
- 样例数据：生成报告文件，Telegram 输出简短摘要和报告路径。
