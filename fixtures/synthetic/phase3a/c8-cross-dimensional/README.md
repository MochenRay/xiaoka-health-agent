# Phase 3A C8 Cross-Dimensional Synthetic Fixtures

This fixture set defines the static report contract for C8 cross-dimensional
observations. It does not generate real reports, does not touch OpenClaw
runtime behavior, and does not contain real health data.

Every daily JSON `notes` field must include the `SYNTHETIC_C8` marker and state
that the record is fabricated or not real health data.

Scenarios:

- `sufficient/`: three effective daily JSON files for 2026-06-01 through
  2026-06-03. Each day has nutrition, exercise/activity, and sleep data, so
  expected weekly and monthly reports may use low-strength observation wording
  such as `观察到`, `可能相关`, or `值得继续观察`.
- `insufficient/`: two effective daily JSON files for 2026-06-01 through
  2026-06-02, with fewer than three paired days. Expected weekly and monthly
  reports must include `数据不足，暂不做关联判断。` and must not add relationship,
  trend, causal, diagnostic, or prescription language.

Expected reports live under each scenario:

- `expected/workspace/reports/weekly-2026-06-07.md`
- `expected/workspace/reports/monthly-2026-06.md`

Validate with:

```bash
python3 scripts/validate_phase3a_c8_fixtures.py
```
