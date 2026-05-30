# Phase 2C Screenshot Fallback Fixtures

These fixtures validate the legacy screenshot fallback contract without using
personal health data, Google Health API responses, or Apple Health export files.
As of 2026-05-28, Google Health API is the primary path for steps, sleep, and
exercise device data.

They intentionally avoid real screenshots. The `recognized/` JSON files are
synthetic, already-confirmed OCR/Vision results for single screenshots. The
paired Markdown log shows the fixed A4/A6 append format, and the paired
`expected/` JSON shows the expected settlement shape under `docs/data-schema.md`.
The `rejected/` JSON files are synthetic OCR/Vision results that must not be
appended because key fields are missing or confidence is too low.

This validates:

- Apple Watch workout screenshot fields: date, workout type, duration, active
  calories, source.
- Apple Health activity summary screenshot fields: date, steps, active
  calories, source.
- Apple Health sleep screenshot fields: date, sleep duration, source.
- The mapping from confirmed screenshot recognition results to Markdown entries
  and expected standard daily JSON.
- Rejection of low-confidence or incomplete screenshot recognition results
  before they can reach the append format.

This does not validate OCR quality, binary image rendering, runtime settlement,
Google Health API import, Apple Health XML, Health Auto Export, or any
historical batch import parser.

Run:

```bash
python3 scripts/validate_phase2c_screenshot_fixtures.py
```
