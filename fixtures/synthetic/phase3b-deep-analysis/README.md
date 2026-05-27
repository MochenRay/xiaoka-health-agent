# Phase 3B M1/E1/S1 Deep-Analysis Synthetic Fixtures

This fixture set documents the static repo-level contract for M1 medication,
E1 exercise, and S1 sleep structured summaries. It does not run OpenClaw cron,
does not contain personal health data, and does not prove runtime report
generation.

Every sample daily JSON `notes` field includes the `SYNTHETIC_PHASE3B` marker.

Files:

- `workspace/data/2026-07/01.json`: one fabricated daily JSON containing
  optional `analysis_summaries.m1_medication`, `analysis_summaries.e1_exercise`,
  and `analysis_summaries.s1_sleep`.
- `expected/weekly-report-sections.md`: expected conservative weekly report
  wording for the three deep-analysis sections.
- `expected/monthly-report-sections.md`: expected conservative monthly report
  wording for the three deep-analysis sections.

Scenario intent:

- M1 is `background_only`: reports must not infer medication effects,
  adherence, dose changes, or clinical decisions.
- E1 is `insufficient_data`: one synthetic exercise day is enough for a record
  recap, not for training trend claims.
- S1 is `insufficient_data`: one synthetic sleep day is enough for current
  observation, not for regularity or sleep-disorder claims.

Validate the fixture JSON with the repository contract validator:

```bash
python3 scripts/validate_repository_contract.py
```
