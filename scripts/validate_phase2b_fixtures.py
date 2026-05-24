#!/usr/bin/env python3
"""Validate Phase 2B synthetic report fixtures."""

from __future__ import annotations

import calendar
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "synthetic" / "phase2b" / "workspace" / "data"
MARKER = "SYNTHETIC_PHASE2B"
EXPECTED_DATES = {
    date(2026, 4, 1),
    date(2026, 4, 2),
    date(2026, 4, 3),
    date(2026, 5, 11),
    date(2026, 5, 12),
    date(2026, 5, 13),
}


def daterange(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def fixture_path(day: date) -> Path:
    return FIXTURE_ROOT / day.strftime("%Y-%m") / f"{day.day:02d}.json"


def date_from_path(path: Path) -> date:
    try:
        return date.fromisoformat(f"{path.parent.name}-{path.stem}")
    except ValueError as exc:
        raise ValueError(f"{path}: path must be YYYY-MM/DD.json") from exc


def load_fixture(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_file(path: Path) -> None:
    data = load_fixture(path)
    expected_date = date_from_path(path).isoformat()
    actual_date = data.get("date")
    if actual_date != expected_date:
        raise ValueError(f"{path}: date must be {expected_date}, got {actual_date!r}")
    notes = data.get("notes")
    if not isinstance(notes, str) or MARKER not in notes:
        raise ValueError(f"{path}: notes must include {MARKER}")
    validate_daily_schema(path, data)


def require_number(path: Path, data: dict, key: str) -> None:
    value = data.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{path}: {key} must be a number")


def validate_daily_schema(path: Path, data: dict) -> None:
    weight = data.get("weight")
    if weight is not None and not isinstance(weight, dict):
        raise ValueError(f"{path}: weight must be null or an object")

    nutrition = data.get("nutrition")
    if not isinstance(nutrition, dict):
        raise ValueError(f"{path}: nutrition must be an object")
    for key in ("total_calories", "protein_g", "carbs_g", "fat_g"):
        require_number(path, nutrition, key)
    meals = nutrition.get("meals")
    if not isinstance(meals, list):
        raise ValueError(f"{path}: nutrition.meals must be a list")

    exercise = data.get("exercise")
    if not isinstance(exercise, dict):
        raise ValueError(f"{path}: exercise must be an object")
    require_number(path, exercise, "total_burn")
    activities = exercise.get("activities")
    if not isinstance(activities, list) or not activities:
        raise ValueError(f"{path}: exercise.activities must be a non-empty list")
    for index, activity in enumerate(activities):
        if not isinstance(activity, dict):
            raise ValueError(f"{path}: exercise.activities[{index}] must be an object")
        activity_path = Path(f"{path}:exercise.activities[{index}]")
        if not isinstance(activity.get("type"), str) or not activity["type"]:
            raise ValueError(f"{activity_path}: type must be a non-empty string")
        require_number(activity_path, activity, "duration_min")
        require_number(activity_path, activity, "calories")
        if not isinstance(activity.get("source"), str) or not activity["source"]:
            raise ValueError(f"{activity_path}: source must be a non-empty string")

    sleep = data.get("sleep")
    if not isinstance(sleep, dict):
        raise ValueError(f"{path}: sleep must be an object")
    require_number(path, sleep, "duration_h")
    quality = sleep.get("quality")
    if quality not in ("good", "fair", "poor", None):
        raise ValueError(f"{path}: sleep.quality must be good, fair, poor, or null")

    supplements = data.get("supplements")
    if not isinstance(supplements, list):
        raise ValueError(f"{path}: supplements must be a list")


def count_coverage(days: list[date]) -> int:
    return sum(1 for day in days if fixture_path(day).exists())


def main() -> int:
    files = sorted(FIXTURE_ROOT.glob("*/*.json"))
    if not files:
        raise SystemExit("No Phase 2B fixture JSON files found")
    actual_dates = {date_from_path(path) for path in files}
    if actual_dates != EXPECTED_DATES:
        expected = ", ".join(sorted(day.isoformat() for day in EXPECTED_DATES))
        actual = ", ".join(sorted(day.isoformat() for day in actual_dates))
        raise ValueError(f"Expected fixture dates [{expected}], got [{actual}]")

    for path in files:
        validate_file(path)

    week_days = list(daterange(date(2026, 5, 11), date(2026, 5, 17)))
    april_days = [date(2026, 4, day) for day in range(1, calendar.monthrange(2026, 4)[1] + 1)]

    week_count = count_coverage(week_days)
    april_count = count_coverage(april_days)

    if week_count != 3:
        raise ValueError(f"Expected 2026-05-11..17 coverage 3/7, got {week_count}/7")
    if april_count != 3:
        raise ValueError(f"Expected 2026-04 coverage 3/30, got {april_count}/30")

    print(f"validated {len(files)} JSON fixture files")
    print("coverage 2026-05-11..2026-05-17: 3/7")
    print("coverage 2026-04: 3/30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
