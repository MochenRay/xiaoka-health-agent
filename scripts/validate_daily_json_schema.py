#!/usr/bin/env python3
"""Validate synthetic daily JSON fixture contracts."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "synthetic"
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
DAY_FILE_RE = re.compile(r"^\d{2}\.json$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"\b(?:\+?86[- ]?)?1[3-9]\d{9}\b")
CHINA_ID_RE = re.compile(r"\b\d{17}[\dXx]\b")

OPTIONAL_OBJECT_FIELDS = (
    "weight",
    "nutrition",
    "exercise",
    "activity_summary",
    "steps",
    "sleep",
)
REAL_PERSON_MARKERS = (
    "真实姓名",
    "身份证",
    "手机号",
    "微信号",
    "wechat:",
    "telegram chat",
    "chat_id",
    "real person",
    "real user",
)
SYNTHETIC_MARKERS = ("SYNTHETIC", "fabricated")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_daily_json_fixture(path: Path) -> bool:
    parts = path.relative_to(FIXTURE_ROOT).parts
    for index in range(len(parts) - 3):
        if (
            parts[index] == "workspace"
            and parts[index + 1] == "data"
            and MONTH_RE.fullmatch(parts[index + 2])
            and DAY_FILE_RE.fullmatch(parts[index + 3])
        ):
            return True
    return False


def date_from_path(path: Path) -> date:
    try:
        return date.fromisoformat(f"{path.parent.name}-{path.stem}")
    except ValueError as exc:
        raise ValueError(f"{relative(path)}: path must end with YYYY-MM/DD.json") from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{relative(path)}: expected a JSON object")
    return data


def require_number(path: Path, value: Any, label: str) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{relative(path)}: {label} must be a number when present")


def validate_optional_object(path: Path, data: dict[str, Any], key: str) -> dict[str, Any] | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{relative(path)}: {key} must be an object or null")
    return value


def validate_synthetic_marker(path: Path, data: dict[str, Any]) -> None:
    notes = data.get("notes")
    if not isinstance(notes, str):
        raise ValueError(f"{relative(path)}: notes must mark the fixture as synthetic")
    if not any(marker in notes for marker in SYNTHETIC_MARKERS):
        raise ValueError(f"{relative(path)}: notes must include a synthetic/fabricated marker")
    lowered = notes.lower()
    if "not real health data" not in lowered and "fabricated" not in lowered:
        raise ValueError(f"{relative(path)}: notes must state the data is not real or fabricated")


def validate_no_real_person_markers(path: Path, data: dict[str, Any]) -> None:
    text = json.dumps(data, ensure_ascii=False)
    lowered = text.lower()
    for marker in REAL_PERSON_MARKERS:
        if marker in lowered:
            raise ValueError(f"{relative(path)}: forbidden real-person marker {marker!r}")
    for pattern, label in (
        (EMAIL_RE, "email address"),
        (PHONE_RE, "phone number"),
        (CHINA_ID_RE, "Chinese national ID"),
    ):
        if pattern.search(text):
            raise ValueError(f"{relative(path)}: forbidden real-person marker: {label}")


def validate_date(path: Path, data: dict[str, Any]) -> None:
    expected = date_from_path(path).isoformat()
    actual = data.get("date")
    if not isinstance(actual, str) or not DATE_RE.fullmatch(actual):
        raise ValueError(f"{relative(path)}: date must be YYYY-MM-DD")
    try:
        date.fromisoformat(actual)
    except ValueError as exc:
        raise ValueError(f"{relative(path)}: invalid date {actual!r}") from exc
    if actual != expected:
        raise ValueError(f"{relative(path)}: date must match path date {expected}, got {actual!r}")


def validate_weight(path: Path, data: dict[str, Any]) -> None:
    weight = validate_optional_object(path, data, "weight")
    if weight is None:
        return
    require_number(path, weight.get("value"), "weight.value")


def validate_nutrition(path: Path, data: dict[str, Any]) -> None:
    nutrition = validate_optional_object(path, data, "nutrition")
    if nutrition is None:
        return
    for key in ("total_calories", "protein_g", "carbs_g", "fat_g"):
        require_number(path, nutrition.get(key), f"nutrition.{key}")
    meals = nutrition.get("meals")
    if meals is not None and not isinstance(meals, list):
        raise ValueError(f"{relative(path)}: nutrition.meals must be a list when present")
    for index, meal in enumerate(meals or []):
        if not isinstance(meal, dict):
            raise ValueError(f"{relative(path)}: nutrition.meals[{index}] must be an object")
        require_number(path, meal.get("calories"), f"nutrition.meals[{index}].calories")
        items = meal.get("items")
        if items is not None and not isinstance(items, list):
            raise ValueError(f"{relative(path)}: nutrition.meals[{index}].items must be a list")
        for item_index, item in enumerate(items or []):
            if not isinstance(item, dict):
                raise ValueError(
                    f"{relative(path)}: nutrition.meals[{index}].items[{item_index}] must be an object"
                )
            for key in ("calories", "protein", "carbs", "fat"):
                require_number(
                    path,
                    item.get(key),
                    f"nutrition.meals[{index}].items[{item_index}].{key}",
                )


def validate_exercise(path: Path, data: dict[str, Any]) -> None:
    exercise = validate_optional_object(path, data, "exercise")
    if exercise is None:
        return
    require_number(path, exercise.get("total_burn"), "exercise.total_burn")
    activities = exercise.get("activities")
    if activities is not None and not isinstance(activities, list):
        raise ValueError(f"{relative(path)}: exercise.activities must be a list when present")
    for index, activity in enumerate(activities or []):
        if not isinstance(activity, dict):
            raise ValueError(f"{relative(path)}: exercise.activities[{index}] must be an object")
        for key in ("duration_min", "calories", "active_energy_kcal", "distance_km", "steps"):
            require_number(path, activity.get(key), f"exercise.activities[{index}].{key}")


def validate_activity_summary(path: Path, data: dict[str, Any]) -> None:
    summary = validate_optional_object(path, data, "activity_summary")
    if summary is None:
        return
    require_number(path, summary.get("active_energy_kcal"), "activity_summary.active_energy_kcal")


def validate_steps(path: Path, data: dict[str, Any]) -> None:
    steps = validate_optional_object(path, data, "steps")
    if steps is None:
        return
    require_number(path, steps.get("count"), "steps.count")


def validate_sleep(path: Path, data: dict[str, Any]) -> None:
    sleep = validate_optional_object(path, data, "sleep")
    if sleep is None:
        return
    for key in ("duration_h", "time_in_bed_h", "efficiency_pct"):
        require_number(path, sleep.get(key), f"sleep.{key}")
    stages = sleep.get("stages")
    if stages is not None and not isinstance(stages, dict):
        raise ValueError(f"{relative(path)}: sleep.stages must be an object when present")
    for key in ("awake_min", "rem_min", "core_min", "deep_min"):
        if isinstance(stages, dict):
            require_number(path, stages.get(key), f"sleep.stages.{key}")


def validate_supplements(path: Path, data: dict[str, Any]) -> None:
    supplements = data.get("supplements")
    if supplements is not None and not isinstance(supplements, list):
        raise ValueError(f"{relative(path)}: supplements must be a list or null")


def validate_file(path: Path) -> None:
    data = load_json(path)
    validate_date(path, data)
    for key in OPTIONAL_OBJECT_FIELDS:
        validate_optional_object(path, data, key)
    validate_weight(path, data)
    validate_nutrition(path, data)
    validate_exercise(path, data)
    validate_activity_summary(path, data)
    validate_steps(path, data)
    validate_sleep(path, data)
    validate_supplements(path, data)
    validate_synthetic_marker(path, data)
    validate_no_real_person_markers(path, data)


def main() -> int:
    files = sorted(path for path in FIXTURE_ROOT.glob("**/*.json") if is_daily_json_fixture(path))
    if not files:
        raise SystemExit("No synthetic daily JSON fixtures found")
    for path in files:
        validate_file(path)
    print(f"validated synthetic daily JSON fixtures: {len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
