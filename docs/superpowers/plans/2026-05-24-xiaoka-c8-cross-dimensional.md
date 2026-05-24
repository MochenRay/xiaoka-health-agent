# Xiaoka C8 Cross-Dimensional Insights Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote C8 cross-dimensional insights from roadmap placeholder to a first-class workflow and static report contract.

**Architecture:** C8 remains a contract-driven agent workflow, not a new runtime service. It reads existing daily JSON and report context, writes no private health data, and uses synthetic fixtures plus a validator to prove both sufficient-data and insufficient-data behavior.

**Tech Stack:** Markdown workflow docs, existing daily JSON schema, Python 3 validator, synthetic fixtures under `fixtures/synthetic/`.

---

## File And Responsibility Map

- `SKILL.md`: add C8 route and workflow contract.
- `docs/c8-cross-dimensional-insights.md`: durable C8 behavior contract.
- `docs/report-automation.md`: connect C8 rules to weekly/monthly prompt contracts.
- `templates/weekly-report.md`: make the C8 report section explicit.
- `templates/monthly-report.md`: make the C8 report section explicit.
- `fixtures/synthetic/phase3a/c8-cross-dimensional/`: synthetic sufficient/insufficient report contracts.
- `scripts/validate_phase3a_c8_fixtures.py`: validate C8 fixtures and expected reports.
- `scripts/README.md`: list the new validator.
- `README.md`: update current capability summary after validation exists.
- `plans/xiaoka-project-roadmap-checklist.md`: mark Phase 3A C8 static contract status accurately.

## Task 1: C8 Workflow And Report Contract

**Files:**
- Modify: `SKILL.md`
- Create: `docs/c8-cross-dimensional-insights.md`
- Modify: `docs/report-automation.md`
- Modify: `templates/weekly-report.md`
- Modify: `templates/monthly-report.md`

- [x] Add `C8 跨维度关联分析` as a first-class route before generic Q1.
- [x] Define C8 input scope: `workspace/data/`, `config/profile.md`, `config/goals.md`, optional `workspace/medical/`.
- [x] Define the hard gate: fewer than 3 effective days or fewer than 3 paired days means `数据不足，暂不做关联判断。`
- [x] Define allowed language: observation, possible association, follow-up focus; no diagnosis, prescription, or causal certainty.
- [x] Update weekly and monthly report templates so the C8 section names conclusion, evidence, and boundary.
- [x] Run `git diff --check`.

## Task 2: C8 Synthetic Fixtures And Validator

**Files:**
- Create: `fixtures/synthetic/phase3a/c8-cross-dimensional/README.md`
- Create: `fixtures/synthetic/phase3a/c8-cross-dimensional/sufficient/**`
- Create: `fixtures/synthetic/phase3a/c8-cross-dimensional/insufficient/**`
- Create: `scripts/validate_phase3a_c8_fixtures.py`
- Modify: `scripts/README.md`

- [x] Create sufficient fixtures with at least 3 daily JSON files containing nutrition, weight, exercise/activity, and sleep.
- [x] Create insufficient fixtures with fewer than 3 eligible paired days.
- [x] Add expected weekly and monthly report files for both branches.
- [x] Add nested `.gitignore` allowlists so fixture `workspace/` paths are tracked.
- [x] Implement a validator that checks marker, coverage, paired days, report paths, insufficient refusal, sufficient evidence, and no strong causal or medical overclaim.
- [x] Run `python3 scripts/validate_phase3a_c8_fixtures.py`.

## Task 3: Project Status And Regression Verification

**Files:**
- Modify: `README.md`
- Modify: `plans/xiaoka-project-roadmap-checklist.md`

- [x] Update project status to say C8 static workflow/report contract and synthetic fixtures are complete.
- [x] Keep runtime language conservative: no OpenClaw C8 runtime revalidation has happened in this task.
- [x] Run:

```bash
git diff --check
python3 scripts/validate_phase2b_fixtures.py
python3 scripts/validate_phase2c_screenshot_fixtures.py
python3 scripts/validate_phase3a_c8_fixtures.py
jq empty references/cn-food-db.json
find fixtures/synthetic -name '*.json' -print0 | xargs -0 jq empty
rg -n "导致|证明|诊断|处方|Health Auto Export|apple_health.py|XML 解析|批量导入已支持|parser 已支持|历史批量导入已支持" SKILL.md README.md docs templates plans fixtures scripts
```

Expected: validators pass; `rg` only returns approved negative statements or the validator's forbidden-language checks.
