# Phase 3A C8 Runtime Smoke Plan

> 最近更新：2026-05-27 CST
> 状态：计划已定义，尚未执行。本文不表示 C8 runtime smoke 已通过。

## 目标

验证 Mac Mini OpenClaw 的真实周报/月报 cron 在 synthetic 数据场景下能生成
`## 跨维度观察`，并遵守 C8 合同：

- 数据足够时，输出有依据、低断言强度的观察。
- 数据不足时，固定写 `数据不足，暂不做关联判断。`
- 不输出确定因果、诊断或处方。

## 关键判断

现有周报/月报 cron 按当前日期计算“上一完整周/月”。因此不能直接把
`fixtures/synthetic/phase3a/c8-cross-dimensional/` 中的 `2026-06` fixture
原样复制到 runtime 后运行。

安全做法是把 sufficient/insufficient synthetic C8 数据映射到运行当天对应的
目标周期，再执行 cron；不临时改 cron payload，不改系统时间。

## 前置条件

- 本地、`origin/main`、Mac Mini workspace 均同步到同一提交。
- Mac Mini `~/.openclaw/cron/jobs.json` 已备份。
- 会被覆盖的 `workspace/data/` 与 `workspace/reports/` 目标文件已备份。
- 执行窗口已确认：周报/月报 delivery 为 `announce`，可能向 Telegram 发送摘要。
- 本次只写入 synthetic JSON，不使用、复制或反向生成真实个人健康数据。

## 建议验证矩阵

| 场景 | 目标 | 期望 |
|------|------|------|
| sufficient weekly | 上一完整周内写入 3 天 C8 synthetic JSON | 周报包含 `## 跨维度观察`，结论为弱判断，依据含有效天数/配对日 |
| insufficient weekly | 上一完整周内只写入不足 C8 synthetic JSON | 周报包含固定不足句，不做趋势断言 |
| sufficient monthly | 上一完整月内写入 3 天 C8 synthetic JSON | 月报包含 source-backed C8 观察 |
| insufficient monthly | 上一完整月内只写入不足 C8 synthetic JSON | 月报包含固定不足句 |

## 执行轮廓

1. 只读确认 runtime：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git rev-parse --short HEAD && git status --short --untracked-files=no'
   ssh mac-mini 'jq -r ".jobs[] | select(.agentId==\"xiaoka\") | [.name,.id,(.enabled|tostring),(.schedule|tostring)] | @tsv" ~/.openclaw/cron/jobs.json'
   ```

2. 在 Mac Mini 建备份目录，备份 `jobs.json`、目标 `workspace/data/` 目录和目标
   `workspace/reports/` 文件；将备份路径写入 marker。

3. 将 `fixtures/synthetic/phase3a/c8-cross-dimensional/sufficient/` 或
   `insufficient/` 中的 JSON 映射到当前 cron 目标周期。映射时必须同步修改
   JSON 内部 `date` 字段，且 `notes` 保留 `SYNTHETIC_C8`。

4. 运行目标 cron 并等待终态：

   ```bash
   ssh mac-mini 'weekly=961c8fcb-9f52-4842-94f6-720202ffa5b2 && before=$(node -e "console.log(Date.now())") && openclaw cron run --wait --expect-final --wait-timeout 10m "$weekly" && openclaw cron runs --id "$weekly" --limit 1 > /tmp/xiaoka-c8-weekly-runs.json && sed -n "/^{/,\$p" /tmp/xiaoka-c8-weekly-runs.json | jq -e --argjson before "$before" ".entries[0] | select(.ts >= \$before and .action == \"finished\" and .status == \"ok\") | {jobId,status,summary,durationMs}"'
   ssh mac-mini 'monthly=51522e31-54dd-495e-8c0e-e8432bb75acd && before=$(node -e "console.log(Date.now())") && openclaw cron run --wait --expect-final --wait-timeout 10m "$monthly" && openclaw cron runs --id "$monthly" --limit 1 > /tmp/xiaoka-c8-monthly-runs.json && sed -n "/^{/,\$p" /tmp/xiaoka-c8-monthly-runs.json | jq -e --argjson before "$before" ".entries[0] | select(.ts >= \$before and .action == \"finished\" and .status == \"ok\") | {jobId,status,summary,durationMs}"'
   ```

5. 检查生成报告：

   ```bash
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && grep -R "## 跨维度观察" workspace/reports/'
   ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && grep -R "数据不足，暂不做关联判断。\\|观察到\\|可能相关\\|值得继续观察" workspace/reports/'
   ```

6. 归档 generated reports 到备份目录，删除 synthetic JSON，恢复原报告。

## 通过标准

- `openclaw cron runs` 新 run 终态为 `ok`。
- 报告含 `## 跨维度观察`、`### 结论`、`### 依据`、`### 边界`。
- sufficient 场景中依据含有效 JSON 天数与候选关联配对日。
- insufficient 场景中结论为固定不足句。
- 报告不含确定因果、诊断、处方或未出现维度的过度声明。
- 验证后 runtime 恢复到执行前状态。

## 与真实截图/OCR Smoke 的关系

真实截图/OCR runtime smoke 是 Phase 2C 的 runtime 验证；C8 runtime smoke 是
报告生成验证。建议顺序：

1. 先做真实截图/OCR runtime smoke，确认截图结果能进入 Markdown 与 daily JSON。
2. 再做 C8 runtime smoke，确认周报/月报能消费 daily JSON 并输出 C8 章节。

若只想评估 C8 报告器，可先用 synthetic JSON 跑 C8 runtime smoke，但公开文案仍
不能宣称真实截图/OCR 已闭环。
