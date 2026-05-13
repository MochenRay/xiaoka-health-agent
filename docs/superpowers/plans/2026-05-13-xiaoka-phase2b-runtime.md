# Xiaoka Phase 2B Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and verify OpenClaw weekly/monthly report cron jobs for Xiaoka without confusing repo truth, OpenClaw workspace truth, and runtime truth.

**Architecture:** The repo already contains the frozen report contract in `docs/report-automation.md` and runtime guardrails in `docs/openclaw-runtime.md`. This plan changes only the Mac Mini OpenClaw runtime after backing up `~/.openclaw/cron/jobs.json`, then verifies jobs through `openclaw cron show/run/runs`; repo docs and checklist are updated only after runtime evidence exists.

**Tech Stack:** OpenClaw CLI 2026.5.2 on `mac-mini`, SSH, `jq`, `python3`, Markdown runtime docs.

---

## File And Runtime Map

- Read: `docs/openclaw-runtime.md`
- Read: `docs/report-automation.md`
- Read: `templates/weekly-report.md`
- Read: `templates/monthly-report.md`
- Modify after runtime verification: `docs/openclaw-runtime.md`
- Modify after runtime verification: `deploy/openclaw-setup.md`
- Modify after runtime verification: `plans/xiaoka-project-roadmap-checklist.md`
- Runtime backup: `mac-mini:~/.openclaw/cron/jobs.json.bak-YYYYMMDD-HHMMSS`
- Runtime modify: `mac-mini:~/.openclaw/cron/jobs.json`
- Runtime read/write by Xiaoka cron: `mac-mini:~/.openclaw/workspace-xiaoka/workspace/reports/`

## Safety Rules

- Do not edit user health data under `config/` or `workspace/` unless a step explicitly says to create a backup first.
- Do not use `crontab`; Xiaoka cron truth is `~/.openclaw/cron/jobs.json`.
- Do not treat `openclaw cron run` enqueue output as success. Always inspect `openclaw cron runs --id "$JOB_ID" --limit 1`.
- Do not mark Phase 2B complete until weekly and monthly jobs have both produced run-history evidence.
- Keep actual Telegram destination out of repo docs. Resolve it from existing Xiaoka jobs at runtime.
- Mac Mini `~/.openclaw/workspace-xiaoka` may contain OpenClaw local untracked files such as `.openclaw/`, `AGENTS.md`, `HEARTBEAT.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, and `memory/`. These are runtime overlays. They are acceptable only if tracked files are clean via `git status --short --untracked-files=no`.
- Enabling jobs or manually running `announce` jobs can send Telegram messages. Stop before Task 5 unless the user has explicitly approved that externally visible action.

### Task 0: Commit Repo Docs And Sync Mac Mini Workspace

**Files:**
- Stage/commit: `README.md`
- Stage/commit: `deploy/openclaw-setup.md`
- Stage/commit: `docs/knowledge-base-sources.md`
- Stage/commit: `docs/openclaw-runtime.md`
- Stage/commit: `docs/report-automation.md`
- Stage/commit: `docs/superpowers/plans/2026-05-13-xiaoka-phase2b-runtime.md`
- Stage/commit: `templates/weekly-report.md`
- Stage/commit: `templates/monthly-report.md`
- Stage/commit: `plans/xiaoka-project-roadmap-checklist.md`
- Runtime sync target: `mac-mini:~/.openclaw/workspace-xiaoka`

- [ ] **Step 1: Verify project repo diff is clean of whitespace errors**

Run:

```bash
git diff --check
```

Expected: exits `0`.

- [ ] **Step 2: Inspect the exact files to stage**

Run:

```bash
git status --short
git diff --stat
git ls-files --others --exclude-standard
```

Expected: only project documentation and template files are modified/untracked. Do not include `config/profile.md`, `config/goals.md`, `workspace/`, or `AI-Shared` files in this project commit.

- [ ] **Step 3: Stage only project repo Phase 2A/2B docs**

Run:

```bash
git add README.md \
  deploy/openclaw-setup.md \
  docs/knowledge-base-sources.md \
  docs/openclaw-runtime.md \
  docs/report-automation.md \
  docs/superpowers/plans/2026-05-13-xiaoka-phase2b-runtime.md \
  templates/weekly-report.md \
  templates/monthly-report.md \
  plans/xiaoka-project-roadmap-checklist.md
git status --short
```

Expected: the listed files are staged; no private runtime files are staged.

- [ ] **Step 4: Commit repo docs**

Run:

```bash
git commit -m "Document phase 2 runtime reporting"
```

Expected: commit succeeds on `main`. Record the new short SHA:

```bash
git rev-parse --short HEAD
```

- [ ] **Step 5: Push repo docs**

Run:

```bash
git push origin main
```

Expected: push succeeds.

- [ ] **Step 6: Pull repo docs into Mac Mini workspace**

Run:

```bash
LOCAL_SHA=$(git rev-parse --short HEAD)
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git pull --ff-only origin main && git rev-parse --short HEAD && git status --short --untracked-files=no && git status --short'
printf 'local=%s\n' "$LOCAL_SHA"
```

Expected: Mac Mini printed SHA equals `local=<same SHA>`, and `git status --short --untracked-files=no` prints nothing. Plain `git status --short` may show known OpenClaw local untracked overlay files; do not delete or stage them.

### Task 1: Runtime Preflight And Backup

**Files:**
- Read: `docs/openclaw-runtime.md`
- Read: `docs/report-automation.md`
- Runtime backup: `mac-mini:~/.openclaw/cron/jobs.json.bak-YYYYMMDD-HHMMSS`

- [ ] **Step 1: Confirm local repo has the runtime plan files**

Run:

```bash
test -f docs/openclaw-runtime.md
test -f docs/report-automation.md
test -f templates/weekly-report.md
test -f templates/monthly-report.md
```

Expected: all commands exit `0`.

- [ ] **Step 2: Confirm Mac Mini workspace baseline**

Run:

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && git branch --show-current && git rev-parse --short HEAD && git status --short --untracked-files=no && git status --short'
```

Expected:

```text
main
```

The second printed line must equal `git rev-parse --short HEAD` from the local repo after Task 0. The `--untracked-files=no` status must print nothing. Plain `git status --short` may show known OpenClaw local untracked overlay files; stop only if tracked files are modified or unknown untracked paths could conflict with repo docs.

- [ ] **Step 3: List existing Xiaoka cron jobs**

Run:

```bash
ssh mac-mini 'openclaw cron list | grep -E "xiaoka|零点结算|结算校验|前日汇总|周报|月报"'
```

Expected: existing `零点结算`、`结算校验`、`前日汇总` rows are present; no Xiaoka `周报` or `月报` rows are present.

- [ ] **Step 4: Back up OpenClaw cron runtime**

Run:

```bash
ssh mac-mini 'set -euo pipefail; backup="$HOME/.openclaw/cron/jobs.json.bak-$(date +%Y%m%d-%H%M%S)"; cp "$HOME/.openclaw/cron/jobs.json" "$backup"; echo "$backup"; test -s "$backup"'
```

Expected: prints a non-empty backup path like `/Users/ray/.openclaw/cron/jobs.json.bak-20260513-184500`.

- [ ] **Step 5: Resolve existing Xiaoka delivery destination without hard-coding it**

Run:

```bash
ssh mac-mini 'jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .delivery.channel==\"telegram\") | .delivery.to" ~/.openclaw/cron/jobs.json | sort -u'
```

Expected: exactly one line. If zero or multiple lines are returned, stop and inspect existing jobs before creating new ones.

### Task 2: Create Weekly Cron Disabled

**Files:**
- Runtime modify: `mac-mini:~/.openclaw/cron/jobs.json`
- Runtime temp file: `mac-mini:/tmp/xiaoka-weekly-message.txt`

- [ ] **Step 1: Write the weekly message payload to a temp file**

Run:

```bash
ssh mac-mini 'cat > /tmp/xiaoka-weekly-message.txt <<'"'"'EOF'"'"'
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
EOF
wc -l /tmp/xiaoka-weekly-message.txt'
```

Expected: `17 /tmp/xiaoka-weekly-message.txt`.

- [ ] **Step 2: Create disabled weekly cron job**

Run:

```bash
ssh mac-mini 'set -euo pipefail
EXISTING=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"周报\") | .id" ~/.openclaw/cron/jobs.json | sed "/^$/d" | wc -l | tr -d " ")
test "$EXISTING" = "0"
CHAT_ID=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .delivery.channel==\"telegram\") | .delivery.to" ~/.openclaw/cron/jobs.json | sort -u)
test "$(printf "%s\n" "$CHAT_ID" | wc -l | tr -d " ")" = "1"
openclaw cron add \
  --name "周报" \
  --agent xiaoka \
  --session isolated \
  --cron "30 8 * * 1" \
  --tz Asia/Shanghai \
  --exact \
  --announce \
  --channel telegram \
  --account xiaoka \
  --to "$CHAT_ID" \
  --timeout-seconds 300 \
  --message "$(cat /tmp/xiaoka-weekly-message.txt)" \
  --disabled \
  --json'
```

Expected: JSON output containing a new job with `"name":"周报"`, `"agentId":"xiaoka"`, and `"enabled":false`.

- [ ] **Step 3: Save weekly job id for later steps**

Run:

```bash
ssh mac-mini 'jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"周报\") | .id" ~/.openclaw/cron/jobs.json'
```

Expected: exactly one UUID.

If this prints zero or more than one UUID, stop. Do not continue with ambiguous job IDs.

### Task 3: Create Monthly Cron Disabled

**Files:**
- Runtime modify: `mac-mini:~/.openclaw/cron/jobs.json`
- Runtime temp file: `mac-mini:/tmp/xiaoka-monthly-message.txt`

- [ ] **Step 1: Write the monthly message payload to a temp file**

Run:

```bash
ssh mac-mini 'cat > /tmp/xiaoka-monthly-message.txt <<'"'"'EOF'"'"'
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
EOF
wc -l /tmp/xiaoka-monthly-message.txt'
```

Expected: `18 /tmp/xiaoka-monthly-message.txt`.

- [ ] **Step 2: Create disabled monthly cron job**

Run:

```bash
ssh mac-mini 'set -euo pipefail
EXISTING=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"月报\") | .id" ~/.openclaw/cron/jobs.json | sed "/^$/d" | wc -l | tr -d " ")
test "$EXISTING" = "0"
CHAT_ID=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .delivery.channel==\"telegram\") | .delivery.to" ~/.openclaw/cron/jobs.json | sort -u)
test "$(printf "%s\n" "$CHAT_ID" | wc -l | tr -d " ")" = "1"
openclaw cron add \
  --name "月报" \
  --agent xiaoka \
  --session isolated \
  --cron "30 8 1 * *" \
  --tz Asia/Shanghai \
  --exact \
  --announce \
  --channel telegram \
  --account xiaoka \
  --to "$CHAT_ID" \
  --timeout-seconds 300 \
  --message "$(cat /tmp/xiaoka-monthly-message.txt)" \
  --disabled \
  --json'
```

Expected: JSON output containing a new job with `"name":"月报"`, `"agentId":"xiaoka"`, and `"enabled":false`.

- [ ] **Step 3: Save monthly job id for later steps**

Run:

```bash
ssh mac-mini 'jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"月报\") | .id" ~/.openclaw/cron/jobs.json'
```

Expected: exactly one UUID.

If this prints zero or more than one UUID, stop. Do not continue with ambiguous job IDs.

### Task 4: Validate Disabled Job Configuration

**Files:**
- Runtime read: `mac-mini:~/.openclaw/cron/jobs.json`

- [ ] **Step 1: Validate weekly job fields**

Run:

```bash
ssh mac-mini 'WEEKLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"周报\") | .id" ~/.openclaw/cron/jobs.json); test "$(printf "%s\n" "$WEEKLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"; WEEKLY_ID="$WEEKLY_IDS"; openclaw cron show "$WEEKLY_ID" --json | jq "{name, agentId, enabled, schedule, delivery, timeoutSeconds: .payload.timeoutSeconds}"'
```

Expected:

```json
{
  "name": "周报",
  "agentId": "xiaoka",
  "enabled": false,
  "schedule": {
    "kind": "cron",
    "expr": "30 8 * * 1",
    "tz": "Asia/Shanghai"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "accountId": "xiaoka"
  },
  "timeoutSeconds": 300
}
```

The actual `delivery.to` may be present in the raw output; do not copy it into repo docs.

- [ ] **Step 2: Validate monthly job fields**

Run:

```bash
ssh mac-mini 'MONTHLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"月报\") | .id" ~/.openclaw/cron/jobs.json); test "$(printf "%s\n" "$MONTHLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"; MONTHLY_ID="$MONTHLY_IDS"; openclaw cron show "$MONTHLY_ID" --json | jq "{name, agentId, enabled, schedule, delivery, timeoutSeconds: .payload.timeoutSeconds}"'
```

Expected:

```json
{
  "name": "月报",
  "agentId": "xiaoka",
  "enabled": false,
  "schedule": {
    "kind": "cron",
    "expr": "30 8 1 * *",
    "tz": "Asia/Shanghai"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "accountId": "xiaoka"
  },
  "timeoutSeconds": 300
}
```

The actual `delivery.to` may be present in the raw output; do not copy it into repo docs.

### Task 5: Enable Jobs And Run Runtime Smoke

External visibility gate: enabling or manually running these jobs may send Telegram messages because delivery mode is `announce`. Do not start this task unless the user has explicitly approved externally visible runtime execution.

**Files:**
- Runtime modify: `mac-mini:~/.openclaw/cron/jobs.json`
- Runtime expected writes: `mac-mini:~/.openclaw/workspace-xiaoka/workspace/reports/weekly-YYYY-MM-DD.md`
- Runtime expected writes: `mac-mini:~/.openclaw/workspace-xiaoka/workspace/reports/monthly-YYYY-MM.md`

- [ ] **Step 1: Enable both jobs**

Run:

```bash
ssh mac-mini 'WEEKLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"周报\") | .id" ~/.openclaw/cron/jobs.json); MONTHLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"月报\") | .id" ~/.openclaw/cron/jobs.json); test "$(printf "%s\n" "$WEEKLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"; test "$(printf "%s\n" "$MONTHLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"; openclaw cron edit "$WEEKLY_IDS" --enable; openclaw cron edit "$MONTHLY_IDS" --enable'
```

Expected: both edit commands exit `0`.

- [ ] **Step 2: Run weekly job manually**

Run:

```bash
ssh mac-mini 'set -euo pipefail
WEEKLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"周报\") | .id" ~/.openclaw/cron/jobs.json)
test "$(printf "%s\n" "$WEEKLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"
WEEKLY_ID="$WEEKLY_IDS"
openclaw cron run "$WEEKLY_ID"
for i in $(seq 1 30); do
  json=$(openclaw cron runs --id "$WEEKLY_ID" --limit 1)
  action=$(printf "%s" "$json" | jq -r ".entries[0].action // empty")
  status=$(printf "%s" "$json" | jq -r ".entries[0].status // empty")
  printf "%s\n" "$json"
  if [ "$action" = "finished" ]; then
    test "$status" = "ok"
    exit 0
  fi
  sleep 10
done
echo "Timed out waiting for weekly cron run to finish" >&2
exit 1'
```

Expected: latest run reaches a terminal successful status. The final output is either exactly `NO_REPLY` for zero coverage, or a short weekly summary plus a `workspace/reports/weekly-YYYY-MM-DD.md` path.

- [ ] **Step 3: Run monthly job manually**

Run:

```bash
ssh mac-mini 'set -euo pipefail
MONTHLY_IDS=$(jq -r ".jobs[] | select(.agentId==\"xiaoka\" and .name==\"月报\") | .id" ~/.openclaw/cron/jobs.json)
test "$(printf "%s\n" "$MONTHLY_IDS" | sed "/^$/d" | wc -l | tr -d " ")" = "1"
MONTHLY_ID="$MONTHLY_IDS"
openclaw cron run "$MONTHLY_ID"
for i in $(seq 1 30); do
  json=$(openclaw cron runs --id "$MONTHLY_ID" --limit 1)
  action=$(printf "%s" "$json" | jq -r ".entries[0].action // empty")
  status=$(printf "%s" "$json" | jq -r ".entries[0].status // empty")
  printf "%s\n" "$json"
  if [ "$action" = "finished" ]; then
    test "$status" = "ok"
    exit 0
  fi
  sleep 10
done
echo "Timed out waiting for monthly cron run to finish" >&2
exit 1'
```

Expected: latest run reaches a terminal successful status. The final output is either exactly `NO_REPLY` for zero coverage, or a short monthly summary plus a `workspace/reports/monthly-YYYY-MM.md` path.

- [ ] **Step 4: Verify report files when output names a path**

Run:

```bash
ssh mac-mini 'cd ~/.openclaw/workspace-xiaoka && find workspace/reports -maxdepth 1 -type f \( -name "weekly-*.md" -o -name "monthly-*.md" \) -print -exec sed -n "1,20p" {} \;'
```

Expected: generated reports start with `# 周报` or `# 月报` and include a coverage line. A zero-coverage run must still write a `0/N` report file; Telegram output should be `NO_REPLY`, not an omitted report file.

### Task 6: Post-Runtime Repo Updates

**Files:**
- Modify: `docs/openclaw-runtime.md`
- Modify: `deploy/openclaw-setup.md`
- Modify: `plans/xiaoka-project-roadmap-checklist.md`

- [ ] **Step 1: Update runtime docs with real job status but not private chat id**

Edit `docs/openclaw-runtime.md` so the `周报` and `月报` rows contain:

Use this shell output to collect the UUIDs:

```bash
ssh mac-mini 'jq -r ".jobs[] | select(.agentId==\"xiaoka\" and (.name==\"周报\" or .name==\"月报\")) | [.name,.id] | @tsv" ~/.openclaw/cron/jobs.json'
```

Then edit the two rows so they contain the real UUIDs and keep the literal redaction token `telegram:<chat_id>` in the Delivery column. Do not write the real Telegram destination into repo files.

- [ ] **Step 2: Update deployment guide status**

Edit `deploy/openclaw-setup.md` so the cron table says:

```markdown
| 周报 | 周一 08:30 | 已存在 | 统计上一个完整自然周，标注覆盖率 |
| 月报 | 每月 1 日 08:30 | 已存在 | 统计上一个完整自然月，标注覆盖率 |
```

- [ ] **Step 3: Update roadmap checklist**

Edit `plans/xiaoka-project-roadmap-checklist.md`:

```markdown
- [x] 添加小卡 `周报` OpenClaw cron job。
- [x] 添加小卡 `月报` OpenClaw cron job。
- [x] 用无数据与样例数据两类场景手动测试 cron。
```

If only zero-coverage `NO_REPLY` was tested and no sample report was produced, keep the sample-data item unchecked and add a note that sample fixture verification remains open.

- [ ] **Step 4: Run repo verification**

Run:

```bash
git diff --check
rg -n --glob '!docs/superpowers/plans/*' '2110286901|qwen3\.5|kimi-k2\.5|周六|月末 20' README.md deploy docs plans templates
```

Expected: `git diff --check` exits `0`; `rg` exits `1` with no matches.

### Task 7: Review And Finish

**Files:**
- Read: all modified files
- Optional stage/commit only if user asked to publish or finish

- [ ] **Step 1: Spec compliance review**

Check:

```bash
grep -n "周报" docs/openclaw-runtime.md
grep -n "月报" docs/openclaw-runtime.md
grep -n "阶段 2B" -A20 plans/xiaoka-project-roadmap-checklist.md
```

Expected: docs say weekly/monthly jobs exist only if runtime evidence exists; checklist does not mark unverified sample-data behavior as complete.

- [ ] **Step 2: Code quality review**

Run:

```bash
git diff -- README.md deploy/openclaw-setup.md docs/openclaw-runtime.md docs/report-automation.md templates/weekly-report.md templates/monthly-report.md plans/xiaoka-project-roadmap-checklist.md
```

Expected: no private chat id, no personal health data, no outdated model recommendations, no claim that Phase 2B is fully complete unless both runtime jobs and verification passed.

- [ ] **Step 3: Final status report**

Report:

Use this exact shape:

```text
Phase 2B runtime:
- Weekly job: created or not created; include the UUID only if it is already present in repo docs.
- Monthly job: created or not created; include the UUID only if it is already present in repo docs.
- Verification: state the latest weekly run status and monthly run status from `openclaw cron runs --id ...`.
- Remaining: name only unchecked checklist items.
```

Do not claim completion without `openclaw cron runs --id ...` evidence.

## Self-Review

- Spec coverage: tasks cover backup, job creation, disabled validation, enablement, run-history verification, docs update, checklist update, and finish review.
- Placeholder scan: the plan uses runtime-resolved variables for chat id and explicit UUID replacement only after creation; no private chat id is hard-coded.
- Type consistency: `周报` uses `30 8 * * 1`, `月报` uses `30 8 1 * *`, both use `agentId=xiaoka`, `session=isolated`, `announce`, `telegram`, `account=xiaoka`, `timeoutSeconds=300`.
