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
    "analysis_summaries",
)
ANALYSIS_SUMMARY_WORKFLOWS = {
    "m1_medication": "M1",
    "e1_exercise": "E1",
    "s1_sleep": "S1",
}
ANALYSIS_SUMMARY_VERSION = "phase3b-static-v1"
ANALYSIS_SUMMARY_STATUSES = (
    "not_run",
    "insufficient_data",
    "background_only",
    "ready",
    "needs_review",
)
M1_MEDICATION_STATUSES = (
    "none_recorded",
    "considering",
    "active",
    "paused",
    "discontinued",
    "unknown",
)
M1_SUPPLEMENT_STATUSES = ("none_recorded", "recorded", "changed", "unknown")
E1_PROGRESSION_SIGNALS = ("improving", "stable", "decreasing", "insufficient_data")
S1_REGULARITY_SIGNALS = ("improving", "stable", "irregular", "mixed", "insufficient_data")
S1_RECOVERY_SIGNALS = ("improving", "stable", "decreasing", "mixed", "insufficient_data")
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


def require_bool(path: Path, value: Any, label: str) -> None:
    if value is None:
        return
    if not isinstance(value, bool):
        raise ValueError(f"{relative(path)}: {label} must be a boolean when present")


def require_string(path: Path, value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{relative(path)}: {label} must be a non-empty string")
    return value


def require_string_list(path: Path, value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{relative(path)}: {label} must be a list")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{relative(path)}: {label}[{index}] must be a non-empty string")
    return value


def require_allowed(path: Path, value: Any, label: str, allowed: tuple[str, ...]) -> str:
    actual = require_string(path, value, label)
    if actual not in allowed:
        raise ValueError(f"{relative(path)}: {label} must be one of {', '.join(allowed)}")
    return actual


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


def validate_summary_period(path: Path, summary: dict[str, Any], label: str) -> None:
    period = summary.get("period")
    if not isinstance(period, dict):
        raise ValueError(f"{relative(path)}: {label}.period must be an object")
    for key in ("start", "end"):
        actual = period.get(key)
        if not isinstance(actual, str) or not DATE_RE.fullmatch(actual):
            raise ValueError(f"{relative(path)}: {label}.period.{key} must be YYYY-MM-DD")
        try:
            date.fromisoformat(actual)
        except ValueError as exc:
            raise ValueError(f"{relative(path)}: invalid {label}.period.{key} {actual!r}") from exc


def validate_m1_trend_inputs(path: Path, trend_inputs: dict[str, Any], label: str) -> None:
    require_allowed(
        path,
        trend_inputs.get("medication_status"),
        f"{label}.trend_inputs.medication_status",
        M1_MEDICATION_STATUSES,
    )
    require_allowed(
        path,
        trend_inputs.get("supplement_status"),
        f"{label}.trend_inputs.supplement_status",
        M1_SUPPLEMENT_STATUSES,
    )
    for key in ("adherence_recorded", "monitoring_needed", "clinician_review_needed"):
        require_bool(path, trend_inputs.get(key), f"{label}.trend_inputs.{key}")
    require_string_list(
        path,
        trend_inputs.get("interaction_flags", []),
        f"{label}.trend_inputs.interaction_flags",
    )


def validate_e1_trend_inputs(path: Path, trend_inputs: dict[str, Any], label: str) -> None:
    for key in ("sessions", "total_duration_min", "total_active_energy_kcal"):
        require_number(path, trend_inputs.get(key), f"{label}.trend_inputs.{key}")
    require_string_list(path, trend_inputs.get("dominant_types", []), f"{label}.trend_inputs.dominant_types")
    require_string_list(path, trend_inputs.get("equipment_used", []), f"{label}.trend_inputs.equipment_used")
    require_bool(
        path,
        trend_inputs.get("injury_constraints_respected"),
        f"{label}.trend_inputs.injury_constraints_respected",
    )
    signal = require_allowed(
        path,
        trend_inputs.get("progression_signal"),
        f"{label}.trend_inputs.progression_signal",
        E1_PROGRESSION_SIGNALS,
    )
    sessions = trend_inputs.get("sessions")
    if isinstance(sessions, (int, float)) and sessions < 3 and signal != "insufficient_data":
        raise ValueError(
            f"{relative(path)}: {label}.trend_inputs.progression_signal must be "
            "insufficient_data when sessions < 3"
        )


def validate_s1_trend_inputs(path: Path, trend_inputs: dict[str, Any], label: str) -> None:
    for key in (
        "sleep_days",
        "avg_duration_h",
        "target_duration_h",
        "avg_efficiency_pct",
        "late_sleep_days",
    ):
        require_number(path, trend_inputs.get(key), f"{label}.trend_inputs.{key}")
    regularity = require_allowed(
        path,
        trend_inputs.get("regularity_signal"),
        f"{label}.trend_inputs.regularity_signal",
        S1_REGULARITY_SIGNALS,
    )
    require_allowed(
        path,
        trend_inputs.get("recovery_signal"),
        f"{label}.trend_inputs.recovery_signal",
        S1_RECOVERY_SIGNALS,
    )
    sleep_days = trend_inputs.get("sleep_days")
    if isinstance(sleep_days, (int, float)) and sleep_days < 3 and regularity != "insufficient_data":
        raise ValueError(
            f"{relative(path)}: {label}.trend_inputs.regularity_signal must be "
            "insufficient_data when sleep_days < 3"
        )


def validate_analysis_summary(path: Path, summary: Any, key: str, workflow: str) -> None:
    label = f"analysis_summaries.{key}"
    if not isinstance(summary, dict):
        raise ValueError(f"{relative(path)}: {label} must be an object")
    actual_workflow = require_string(path, summary.get("workflow"), f"{label}.workflow")
    if actual_workflow != workflow:
        raise ValueError(f"{relative(path)}: {label}.workflow must be {workflow}, got {actual_workflow!r}")
    version = require_string(path, summary.get("version"), f"{label}.version")
    if version != ANALYSIS_SUMMARY_VERSION:
        raise ValueError(
            f"{relative(path)}: {label}.version must be {ANALYSIS_SUMMARY_VERSION}, got {version!r}"
        )
    require_allowed(path, summary.get("status"), f"{label}.status", ANALYSIS_SUMMARY_STATUSES)
    validate_summary_period(path, summary, label)
    require_string_list(path, summary.get("source_scope"), f"{label}.source_scope")
    require_string(path, summary.get("summary"), f"{label}.summary")
    trend_inputs = summary.get("trend_inputs")
    if not isinstance(trend_inputs, dict):
        raise ValueError(f"{relative(path)}: {label}.trend_inputs must be an object")
    require_string_list(path, summary.get("flags", []), f"{label}.flags")
    if "report_carry_forward" not in summary:
        raise ValueError(f"{relative(path)}: {label}.report_carry_forward is required")
    require_bool(path, summary.get("report_carry_forward"), f"{label}.report_carry_forward")

    if workflow == "M1":
        validate_m1_trend_inputs(path, trend_inputs, label)
    elif workflow == "E1":
        validate_e1_trend_inputs(path, trend_inputs, label)
    elif workflow == "S1":
        validate_s1_trend_inputs(path, trend_inputs, label)


def validate_analysis_summaries(path: Path, data: dict[str, Any]) -> None:
    summaries = validate_optional_object(path, data, "analysis_summaries")
    if summaries is None:
        return
    if "phase3b-deep-analysis" in relative(path):
        missing = [key for key in ANALYSIS_SUMMARY_WORKFLOWS if key not in summaries]
        if missing:
            raise ValueError(f"{relative(path)}: missing required Phase 3B summaries: {', '.join(missing)}")
    for key, summary in summaries.items():
        if key not in ANALYSIS_SUMMARY_WORKFLOWS:
            raise ValueError(f"{relative(path)}: unsupported analysis_summaries key {key!r}")
        validate_analysis_summary(path, summary, key, ANALYSIS_SUMMARY_WORKFLOWS[key])


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
    validate_analysis_summaries(path, data)
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
