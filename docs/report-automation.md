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

## Phase 2B Synthetic 本地验证

Phase 2B 的非零覆盖验证使用仓库内 synthetic fixture，不使用真实
`workspace/` 数据：

- fixture 路径：`fixtures/synthetic/phase2b/workspace/data/`
- 周报覆盖目标：`2026-05-11..2026-05-17` 为 `3/7`
- 月报覆盖目标：`2026-04` 为 `3/30`
- 每个 JSON 的 `notes` 必须包含 `SYNTHETIC_PHASE2B`
- fixture 只能人工编写 synthetic 内容，不能从真实 `workspace/` 反向生成

仓库侧验证：

```bash
python3 scripts/validate_phase2b_fixtures.py
jq empty fixtures/synthetic/phase2b/workspace/data/2026-04/*.json
jq empty fixtures/synthetic/phase2b/workspace/data/2026-05/*.json
git diff --check
```

## Phase 2B Mac Mini 安全验证步骤

以下步骤是待执行的 runtime 验证规范。本仓库不记录真实 Telegram chat id，
也不得把“准备执行”写成“已运行成功”。`announce` delivery 可能向 Telegram
发送消息，执行前必须确认接收方、时间窗口和回滚方案。

1. 备份 runtime、目标数据目录和会被覆盖的报告文件。命令会打印本次备份目录，并把
   路径写入 `workspace/.phase2b-backup-current`：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && stamp=$(date +%Y%m%d-%H%M%S) && backup="$HOME/.openclaw/backups/xiaoka-phase2b-synthetic-$stamp" && mkdir -p "$backup/workspace/data" "$backup/workspace/reports" "$backup/generated" && cp ~/.openclaw/cron/jobs.json "$backup/jobs.json" && test ! -e workspace/data/2026-04 || cp -R workspace/data/2026-04 "$backup/workspace/data/" && test ! -e workspace/data/2026-05 || cp -R workspace/data/2026-05 "$backup/workspace/data/" && test ! -e workspace/reports/weekly-2026-05-17.md || cp workspace/reports/weekly-2026-05-17.md "$backup/workspace/reports/" && test ! -e workspace/reports/monthly-2026-04.md || cp workspace/reports/monthly-2026-04.md "$backup/workspace/reports/" && printf "%s\n" "$backup" > workspace/.phase2b-backup-current && printf "%s\n" "$backup"'
   ```

2. 写入 synthetic fixture 到 runtime `workspace/data/`，仅用于验证。若任一目标
   日期已有文件，立即停止，不覆盖真实记录。只复制白名单中的 6 个 fixture，
   不使用目录通配符：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && for f in workspace/data/2026-04/01.json workspace/data/2026-04/02.json workspace/data/2026-04/03.json workspace/data/2026-05/11.json workspace/data/2026-05/12.json workspace/data/2026-05/13.json; do test ! -e "$f" || { echo "refuse to overwrite existing $f"; exit 1; }; done && mkdir -p workspace/data/2026-04 workspace/data/2026-05 && cp fixtures/synthetic/phase2b/workspace/data/2026-04/01.json workspace/data/2026-04/01.json && cp fixtures/synthetic/phase2b/workspace/data/2026-04/02.json workspace/data/2026-04/02.json && cp fixtures/synthetic/phase2b/workspace/data/2026-04/03.json workspace/data/2026-04/03.json && cp fixtures/synthetic/phase2b/workspace/data/2026-05/11.json workspace/data/2026-05/11.json && cp fixtures/synthetic/phase2b/workspace/data/2026-05/12.json workspace/data/2026-05/12.json && cp fixtures/synthetic/phase2b/workspace/data/2026-05/13.json workspace/data/2026-05/13.json'
   ```

3. 运行周报/月报 cron，并等待最终状态。`openclaw cron run` 只表示入队；
   这里使用 `--wait --expect-final` 等待当前 run 完成，再用运行前时间戳验证
   history 中的最新记录是新 run、终态为 `ok`，且 summary 不是 `NO_REPLY`：

   ```bash
   ssh mac-mini 'weekly=961c8fcb-9f52-4842-94f6-720202ffa5b2 && before=$(node -e "console.log(Date.now())") && openclaw cron run --wait --expect-final --wait-timeout 10m "$weekly" && openclaw cron runs --id "$weekly" --limit 1 > /tmp/xiaoka-phase2b-weekly-runs.json && sed -n "/^{/,\$p" /tmp/xiaoka-phase2b-weekly-runs.json | jq -e --argjson before "$before" ".entries[0] | select(.ts >= \$before and .action == \"finished\" and .status == \"ok\" and (.summary // \"\") != \"NO_REPLY\") | {jobId, status, summary, durationMs}"'
   ssh mac-mini 'monthly=51522e31-54dd-495e-8c0e-e8432bb75acd && before=$(node -e "console.log(Date.now())") && openclaw cron run --wait --expect-final --wait-timeout 10m "$monthly" && openclaw cron runs --id "$monthly" --limit 1 > /tmp/xiaoka-phase2b-monthly-runs.json && sed -n "/^{/,\$p" /tmp/xiaoka-phase2b-monthly-runs.json | jq -e --argjson before "$before" ".entries[0] | select(.ts >= \$before and .action == \"finished\" and .status == \"ok\" and (.summary // \"\") != \"NO_REPLY\") | {jobId, status, summary, durationMs}"'
   ```

4. 检查报告与覆盖率：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && grep -R "3/7\\|3 / 7" workspace/reports/weekly-2026-05-17.md'
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && grep -R "3/30\\|3 / 30" workspace/reports/monthly-2026-04.md'
   ```

5. 归档 synthetic 生成报告，再恢复 runtime。此命令即使报告未生成，也会继续删除
   synthetic JSON。只有 `workspace/.phase2b-backup-current` 指向有效备份目录时，
   才会归档、恢复或删除报告；若备份标记缺失，则报告保持原样并返回失败：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && backup=$(cat workspace/.phase2b-backup-current 2>/dev/null || true); rm -f workspace/data/2026-04/01.json workspace/data/2026-04/02.json workspace/data/2026-04/03.json workspace/data/2026-05/11.json workspace/data/2026-05/12.json workspace/data/2026-05/13.json; rmdir workspace/data/2026-04 workspace/data/2026-05 2>/dev/null || true; if test -z "$backup" || test ! -d "$backup"; then echo "missing valid backup marker; synthetic JSON removed, reports left untouched" >&2; exit 1; fi; mkdir -p "$backup/generated"; cp -f workspace/reports/weekly-2026-05-17.md "$backup/generated/" 2>/dev/null || true; cp -f workspace/reports/monthly-2026-04.md "$backup/generated/" 2>/dev/null || true; if test -e "$backup/workspace/reports/weekly-2026-05-17.md"; then cp -f "$backup/workspace/reports/weekly-2026-05-17.md" workspace/reports/weekly-2026-05-17.md; else rm -f workspace/reports/weekly-2026-05-17.md; fi; if test -e "$backup/workspace/reports/monthly-2026-04.md"; then cp -f "$backup/workspace/reports/monthly-2026-04.md" workspace/reports/monthly-2026-04.md; else rm -f workspace/reports/monthly-2026-04.md; fi; rm -f workspace/.phase2b-backup-current; printf "archived generated reports under %s/generated\n" "$backup"'
   ```

6. 记录结果时只写 run id、status、summary 形态、报告路径和覆盖率；不得记录真实
   Telegram chat id 或个人健康数据。
