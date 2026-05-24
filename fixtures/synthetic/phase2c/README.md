# Phase 2C Screenshot-First Fixtures

These fixtures validate the screenshot-first contract without using personal
health data or Apple Health export files.

They intentionally avoid real screenshots. The `recognized/` JSON files are
synthetic, already-confirmed OCR/Vision results for single screenshots. The
paired Markdown log shows the fixed A4/A6 append format, and the paired
`expected/` JSON shows the expected settlement shape under `docs/data-schema.md`.

This validates:

- Apple Watch workout screenshot fields: date, workout type, duration, active
  calories, source.
- Apple Health activity summary screenshot fields: date, steps, active
  calories, source.
- Apple Health sleep screenshot fields: date, sleep duration, source.
- The mapping from confirmed screenshot recognition results to Markdown entries
  and expected standard daily JSON.

This does not validate OCR quality, binary image rendering, runtime settlement,
Apple Health XML, Health Auto Export, or any historical batch import parser.

Run:

```bash
python3 scripts/validate_phase2c_screenshot_fixtures.py
```
