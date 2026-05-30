# Google Health API Synthetic Fixture

This fixture validates the repo-layer Google Health API importer without OAuth,
network access, raw API response persistence, or personal health data.

It covers:

- `steps` daily rollup from a `HEALTH_KIT` / Apple Health source.
- `sleep` data point from a `HEALTH_KIT` / Apple Health source.
- `exercise` data point from a `HEALTH_KIT` / Apple Fitness source.
- Normalized records that can be appended idempotently to
  `workspace/logs/YYYY-MM/DD.md`.

This does not validate a real Google OAuth flow, token refresh, API quota,
OpenClaw cron execution, runtime settlement, or daily JSON generation.

Run:

```bash
python3 scripts/validate_google_health_importer.py
```

Inspect dry-run records:

```bash
python3 scripts/import_google_health.py \
  --fixture-input fixtures/synthetic/google-health-api/google-health-api-synthetic.json \
  --dry-run
```
