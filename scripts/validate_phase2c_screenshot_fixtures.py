#!/usr/bin/env python3
"""Validate Phase 2C screenshot-first fixture contracts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "synthetic" / "phase2c"
RECOGNIZED = FIXTURE_ROOT / "recognized"
LOG_PATH = FIXTURE_ROOT / "workspace" / "logs" / "2026-05" / "18.md"
JSON_PATH = FIXTURE_ROOT / "expected" / "workspace" / "data" / "2026-05" / "18.json"
MARKER = "SYNTHETIC_PHASE2C"

ALLOWED_WORKOUT_SOURCES = {
    "apple_watch_workout_screenshot",
    "apple_health_workout_screenshot",
}
ALLOWED_ACTIVITY_SOURCES = {
    "apple_health_activity_screenshot",
    "apple_watch_activity_screenshot",
}
ALLOWED_SLEEP_SOURCES = {
    "apple_health_sleep_screenshot",
    "apple_watch_sleep_screenshot",
}
ALLOWED_CONFIDENCES = {"high", "medium"}
EXPECTED_RECOGNIZED_FILES = {
    "activity-summary-apple-health.json",
    "sleep-apple-health.json",
    "workout-apple-watch.json",
}


def load_recognized(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    if data.get("marker") != MARKER:
        raise ValueError(f"{path}: marker must be {MARKER}")
    return data


def require_keys(path: Path, values: dict, keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if not values.get(key)]
    if missing:
        raise ValueError(f"{path}: missing required keys: {', '.join(missing)}")


def require_number(values: dict, key: str) -> None:
    value = values.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{key} must be numeric, got {value!r}")


def markdown_value(value) -> str:
    if value is None:
        return "null"
    return str(value)


def markdown_tables(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        if index + 1 >= len(lines) or not lines[index + 1].strip().startswith("|"):
            continue
        divider = [cell.strip() for cell in lines[index + 1].strip().strip("|").split("|")]
        if not divider or not all(set(cell) <= {"-", ":"} for cell in divider):
            continue
        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        row_index = index + 2
        while row_index < len(lines) and lines[row_index].strip().startswith("|"):
            values = [cell.strip() for cell in lines[row_index].strip().strip("|").split("|")]
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
            row_index += 1
    return rows


def find_row(rows: list[dict[str, str]], **criteria: str) -> dict[str, str]:
    for row in rows:
        if all(row.get(key) == value for key, value in criteria.items()):
            return row
    criteria_text = ", ".join(f"{key}={value!r}" for key, value in criteria.items())
    raise ValueError(f"missing markdown row matching {criteria_text}")


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    if MARKER not in str(data.get("notes", "")):
        raise ValueError(f"{path}: notes must include {MARKER}")
    return data


def assert_equal(label: str, actual, expected) -> None:
    if actual != expected:
        raise ValueError(f"{label}: expected {expected!r}, got {actual!r}")


def validate_recognized(workout: dict, activity: dict, sleep: dict) -> None:
    actual_files = {path.name for path in RECOGNIZED.glob("*.json")}
    if actual_files != EXPECTED_RECOGNIZED_FILES:
        raise ValueError(
            "recognized fixtures must exactly match "
            f"{sorted(EXPECTED_RECOGNIZED_FILES)}, got {sorted(actual_files)}"
        )

    require_keys(
        RECOGNIZED / "workout-apple-watch.json",
        workout,
        ("kind", "source", "date", "type", "duration_min", "active_energy_kcal", "confidence"),
    )
    assert_equal("workout kind", workout["kind"], "workout")
    for key in ("duration_min", "active_energy_kcal"):
        require_number(workout, key)
    for key in ("steps", "distance_km"):
        require_number(workout, key)
    for key in ("start_time", "end_time"):
        if not isinstance(workout.get(key), str) or not workout[key]:
            raise ValueError(f"workout {key} must be a non-empty string")
    if workout["source"] not in ALLOWED_WORKOUT_SOURCES:
        raise ValueError(f"unexpected workout source {workout['source']!r}")
    if workout["confidence"] not in ALLOWED_CONFIDENCES:
        raise ValueError("workout confidence must be high or medium; low requires user confirmation")

    require_keys(
        RECOGNIZED / "activity-summary-apple-health.json",
        activity,
        ("kind", "source", "date", "steps", "active_energy_kcal", "confidence"),
    )
    assert_equal("activity kind", activity["kind"], "activity_summary")
    for key in ("steps", "active_energy_kcal"):
        require_number(activity, key)
    if activity["source"] not in ALLOWED_ACTIVITY_SOURCES:
        raise ValueError(f"unexpected activity source {activity['source']!r}")
    if activity["confidence"] not in ALLOWED_CONFIDENCES:
        raise ValueError("activity confidence must be high or medium; low requires user confirmation")

    require_keys(
        RECOGNIZED / "sleep-apple-health.json",
        sleep,
        ("kind", "source", "date", "duration_h", "confidence"),
    )
    assert_equal("sleep kind", sleep["kind"], "sleep")
    require_number(sleep, "duration_h")
    for key in ("time_in_bed_h", "efficiency_pct"):
        require_number(sleep, key)
    for key in ("start_time", "end_time"):
        if not isinstance(sleep.get(key), str) or not sleep[key]:
            raise ValueError(f"sleep {key} must be a non-empty string")
    if sleep.get("quality") not in ("good", "fair", "poor", None):
        raise ValueError("sleep quality must be good, fair, poor, or null")
    stages = sleep.get("stages")
    if not isinstance(stages, dict):
        raise ValueError("sleep stages must be an object")
    for key in ("awake_min", "rem_min", "core_min", "deep_min"):
        require_number(stages, key)
    if sleep["source"] not in ALLOWED_SLEEP_SOURCES:
        raise ValueError(f"unexpected sleep source {sleep['source']!r}")
    if sleep["confidence"] not in ALLOWED_CONFIDENCES:
        raise ValueError("sleep confidence must be high or medium; low requires user confirmation")


def validate_log(log_text: str, workout: dict, activity: dict, sleep: dict) -> None:
    if MARKER not in log_text:
        raise ValueError(f"{LOG_PATH}: must include {MARKER}")
    rows = markdown_tables(log_text)

    workout_row = find_row(rows, 日期=workout["date"], 类型=workout["type"])
    assert_equal("workout duration", workout_row["时长min"], str(workout["duration_min"]))
    assert_equal("workout active calories", workout_row["active calories"], str(workout["active_energy_kcal"]))
    assert_equal("workout source", workout_row["来源"], workout["source"])
    workout_note = workout_row.get("备注", "")
    for expected in (
        f"steps {workout['steps']}",
        f"distance {workout['distance_km']}km",
        f"end {workout['end_time']}",
        f"confidence {workout['confidence']}",
    ):
        if expected not in workout_note:
            raise ValueError(f"workout markdown note must include {expected!r}")

    activity_row = find_row(rows, 日期=activity["date"], steps=str(activity["steps"]))
    assert_equal("activity active calories", activity_row["active calories"], str(activity["active_energy_kcal"]))
    assert_equal("activity source", activity_row["来源"], activity["source"])
    activity_note = activity_row.get("备注", "")
    if "day-level activity summary" not in activity_note:
        raise ValueError("activity markdown note must mark the row as day-level summary")
    if f"confidence {activity['confidence']}" not in activity_note:
        raise ValueError("activity markdown note must include confidence")

    sleep_row = find_row(rows, 日期=sleep["date"], 来源=sleep["source"])
    assert_equal("sleep duration", sleep_row["睡眠时长h"], str(sleep["duration_h"]))
    if sleep.get("start_time"):
        assert_equal("sleep start", sleep_row["开始"], sleep["start_time"])
    if sleep.get("end_time"):
        assert_equal("sleep end", sleep_row["结束"], sleep["end_time"])
    assert_equal("sleep quality", sleep_row["质量"], markdown_value(sleep["quality"]))
    sleep_note = sleep_row.get("备注", "")
    for key, label in (
        ("time_in_bed_h", "time in bed"),
        ("efficiency_pct", "efficiency"),
        ("confidence", "confidence"),
    ):
        if f"{label} {sleep[key]}" not in sleep_note:
            raise ValueError(f"sleep markdown note must include {label} {sleep[key]}")
    for key, label in (
        ("awake_min", "awake"),
        ("rem_min", "REM"),
        ("core_min", "core"),
        ("deep_min", "deep"),
    ):
        expected = f"{label} {sleep['stages'][key]}min"
        if expected not in sleep_note:
            raise ValueError(f"sleep markdown note must include {expected!r}")


def validate_json(data: dict, workout: dict, activity: dict, sleep: dict) -> None:
    assert_equal("date", data.get("date"), workout["date"])
    assert_equal("activity date", activity["date"], workout["date"])
    assert_equal("sleep date", sleep["date"], workout["date"])

    exercise = data.get("exercise")
    if not isinstance(exercise, dict):
        raise ValueError("exercise must be an object")
    activities = exercise.get("activities")
    if not isinstance(activities, list) or len(activities) != 1:
        raise ValueError("exercise.activities must contain exactly one workout fixture")
    item = activities[0]
    assert_equal("json workout type", item.get("type"), workout["type"])
    assert_equal("json workout duration", item.get("duration_min"), workout["duration_min"])
    assert_equal("json workout calories", item.get("active_energy_kcal"), workout["active_energy_kcal"])
    assert_equal("json workout source", item.get("source"), workout["source"])
    assert_equal("json workout confidence", item.get("confidence"), workout["confidence"])
    assert_equal("json workout steps", item.get("steps"), workout["steps"])
    assert_equal("json workout distance", item.get("distance_km"), workout["distance_km"])
    assert_equal("json workout start", item.get("start_time"), workout["start_time"])
    assert_equal("json workout end", item.get("end_time"), workout["end_time"])
    if MARKER not in str(item.get("note", "")):
        raise ValueError("json workout note must include marker")

    summary = data.get("activity_summary")
    if not isinstance(summary, dict):
        raise ValueError("activity_summary must be an object")
    assert_equal("json activity energy", summary.get("active_energy_kcal"), activity["active_energy_kcal"])
    assert_equal("json activity source", summary.get("source"), activity["source"])
    assert_equal("json activity confidence", summary.get("confidence"), activity["confidence"])
    if MARKER not in str(summary.get("note", "")):
        raise ValueError("json activity note must include marker")

    steps = data.get("steps")
    if not isinstance(steps, dict):
        raise ValueError("steps must be an object")
    assert_equal("json steps", steps.get("count"), activity["steps"])
    assert_equal("json steps source", steps.get("source"), activity["source"])

    sleep_json = data.get("sleep")
    if not isinstance(sleep_json, dict):
        raise ValueError("sleep must be an object")
    assert_equal("json sleep duration", sleep_json.get("duration_h"), sleep["duration_h"])
    assert_equal("json sleep source", sleep_json.get("source"), sleep["source"])
    assert_equal("json sleep confidence", sleep_json.get("confidence"), sleep["confidence"])
    assert_equal("json sleep start", sleep_json.get("start_time"), sleep["start_time"])
    assert_equal("json sleep end", sleep_json.get("end_time"), sleep["end_time"])
    assert_equal("json sleep time in bed", sleep_json.get("time_in_bed_h"), sleep["time_in_bed_h"])
    assert_equal("json sleep efficiency", sleep_json.get("efficiency_pct"), sleep["efficiency_pct"])
    assert_equal("json sleep quality", sleep_json.get("quality"), sleep["quality"])
    if MARKER not in str(sleep_json.get("note", "")):
        raise ValueError("json sleep note must include marker")

    stages = sleep_json.get("stages")
    if not isinstance(stages, dict):
        raise ValueError("sleep.stages must be an object")
    recognized_stages = sleep.get("stages")
    if not isinstance(recognized_stages, dict):
        raise ValueError("recognized sleep.stages must be an object")
    for key in ("awake_min", "rem_min", "core_min", "deep_min"):
        assert_equal(f"json sleep {key}", stages.get(key), recognized_stages[key])


def main() -> int:
    workout = load_recognized(RECOGNIZED / "workout-apple-watch.json")
    activity = load_recognized(RECOGNIZED / "activity-summary-apple-health.json")
    sleep = load_recognized(RECOGNIZED / "sleep-apple-health.json")
    validate_recognized(workout, activity, sleep)

    log_text = LOG_PATH.read_text(encoding="utf-8")
    validate_log(log_text, workout, activity, sleep)

    data = load_json(JSON_PATH)
    validate_json(data, workout, activity, sleep)

    print("validated Phase 2C screenshot-first fixtures")
    print("covered: workout screenshot, activity summary screenshot, sleep screenshot")
    print("validated mapping: recognized result -> Markdown append shape -> expected daily JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
