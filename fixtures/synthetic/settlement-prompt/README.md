# Settlement Prompt Synthetic Fixture

This fixture set documents one repo-layer regression case for the zero-nightly
settlement prompt contract. It does not run OpenClaw cron, does not contain
personal health data, and does not prove runtime settlement quality.

Files:

- `workspace/logs/2026-07/02.md`: fabricated daily Markdown log with weight,
  meals, exercise, supplements, and sleep.
- `expected/workspace/data/2026-07/02.json`: expected daily JSON shape after
  settlement.

The fixture uses the `SYNTHETIC_SETTLEMENT` marker. Validate it with:

```bash
python3 scripts/validate_settlement_prompt_contract.py
python3 scripts/validate_daily_json_schema.py
```
