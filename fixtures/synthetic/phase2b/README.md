# Phase 2B Synthetic Fixtures

These fixtures are synthetic inputs for local non-zero coverage validation of
weekly and monthly report automation.

They are intentionally stored under `fixtures/synthetic/phase2b/`, not under the
runtime `workspace/` tree. Do not reverse-generate them from a real user
workspace, and do not copy real health records into this directory.

Every fixture must include `SYNTHETIC_PHASE2B` in `notes` so validation and
runtime dry runs can distinguish these files from real personal health data.

Current coverage targets:

- Week `2026-05-11..2026-05-17`: 3 JSON files out of 7 days.
- Month `2026-04`: 3 JSON files out of 30 days.

Validate locally with:

```bash
python3 scripts/validate_phase2b_fixtures.py
```
