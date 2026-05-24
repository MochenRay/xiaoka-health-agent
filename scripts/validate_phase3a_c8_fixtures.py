#!/usr/bin/env python3
"""Validate Phase 3A C8 cross-dimensional synthetic fixtures."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "synthetic" / "phase3a" / "c8-cross-dimensional"
MARKER = "SYNTHETIC_C8"
FABRICATED_TERMS = ("not real health data", "fabricated")
SCENARIOS = {
    "sufficient": {
        "dates": {date(2026, 6, 1), date(2026, 6, 2), date(2026, 6, 3)},
        "weekly_coverage": "覆盖率：有效 JSON 天数 3/7，配对日 3/7。",
        "monthly_coverage": "覆盖率：有效 JSON 天数 3/30，配对日 3/30。",
        "expected_effective_days": 3,
        "expected_paired_days": 3,
        "expected_paired_dates": {date(2026, 6, 1), date(2026, 6, 2), date(2026, 6, 3)},
    },
    "insufficient": {
        "dates": {date(2026, 6, 1), date(2026, 6, 2)},
        "weekly_coverage": "覆盖率：有效 JSON 天数 2/7，配对日 1/7。",
        "monthly_coverage": "覆盖率：有效 JSON 天数 2/30，配对日 1/30。",
        "expected_effective_days": 2,
        "expected_paired_days": 1,
        "expected_paired_dates": {date(2026, 6, 1)},
    },
}
EXPECTED_REPORTS = {
    "weekly-2026-06-07.md": "workspace/reports/weekly-2026-06-07.md",
    "monthly-2026-06.md": "workspace/reports/monthly-2026-06.md",
}
LOW_STRENGTH_TERMS = ("观察到", "可能相关", "值得继续观察")
REQUIRED_METRICS = ("热量", "蛋白质", "体重", "运动/消耗", "睡眠")
FORBIDDEN_STRONG_TERMS = ("导致", "因为", "证明", "诊断", "处方", "因果")
FORBIDDEN_MISSING_DATA_TERMS = FORBIDDEN_STRONG_TERMS + ("相关", "趋势", "因果", "关联")
FORBIDDEN_UNPROVIDED_DIMENSIONS = (
    "医学改善",
    "血检",
    "血糖",
    "血脂",
    "指标改善",
    "药物",
    "用药",
    "体检",
)
INSUFFICIENT_SENTENCE = "数据不足，暂不做关联判断。"


def format_number(value: int | float) -> str:
    if isinstance(value, int) or value.is_integer():
        return str(int(value))
    return f"{value:.1f}"


def format_range(values: list[int | float]) -> str:
    return f"{format_number(min(values))}-{format_number(max(values))}"


def date_from_path(path: Path) -> date:
    try:
        return date.fromisoformat(f"{path.parent.name}-{path.stem}")
    except ValueError as exc:
        raise ValueError(f"{path}: path must be YYYY-MM/DD.json") from exc


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def scenario_data_root(scenario: str) -> Path:
    return FIXTURE_ROOT / scenario / "workspace" / "data"


def scenario_report_root(scenario: str) -> Path:
    return FIXTURE_ROOT / scenario / "expected" / "workspace" / "reports"


def validate_notes(path: Path, data: dict) -> None:
    notes = data.get("notes")
    if not isinstance(notes, str) or MARKER not in notes:
        raise ValueError(f"{path}: notes must include {MARKER}")
    lowered = notes.lower()
    if not any(term in lowered for term in FABRICATED_TERMS):
        raise ValueError(f"{path}: notes must state not real health data or fabricated")


def validate_date(path: Path, data: dict) -> date:
    expected = date_from_path(path)
    actual = data.get("date")
    if actual != expected.isoformat():
        raise ValueError(f"{path}: date must be {expected.isoformat()}, got {actual!r}")
    return expected


def has_number(data: dict, key: str) -> bool:
    value = data.get(key)
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def has_nutrition(data: dict) -> bool:
    nutrition = data.get("nutrition")
    return (
        isinstance(nutrition, dict)
        and has_number(nutrition, "total_calories")
        and has_number(nutrition, "protein_g")
    )


def has_weight(data: dict) -> bool:
    weight = data.get("weight")
    return isinstance(weight, dict) and has_number(weight, "value")


def has_exercise_or_activity(data: dict) -> bool:
    exercise = data.get("exercise")
    if not isinstance(exercise, dict):
        return False
    activities = exercise.get("activities")
    return has_number(exercise, "total_burn") and isinstance(activities, list) and bool(activities)


def has_sleep(data: dict) -> bool:
    sleep = data.get("sleep")
    return isinstance(sleep, dict) and has_number(sleep, "duration_h")


def is_paired_day(data: dict) -> bool:
    return has_nutrition(data) and has_weight(data) and has_exercise_or_activity(data) and has_sleep(data)


def load_scenario_json(scenario: str) -> dict[date, dict]:
    root = scenario_data_root(scenario)
    files = sorted(root.glob("*/*.json"))
    if not files:
        raise ValueError(f"{root}: no JSON fixtures found")

    expected_dates = SCENARIOS[scenario]["dates"]
    actual_dates = {date_from_path(path) for path in files}
    if actual_dates != expected_dates:
        expected = ", ".join(day.isoformat() for day in sorted(expected_dates))
        actual = ", ".join(day.isoformat() for day in sorted(actual_dates))
        raise ValueError(f"{scenario}: expected dates [{expected}], got [{actual}]")

    by_date: dict[date, dict] = {}
    for path in files:
        data = load_json(path)
        day = validate_date(path, data)
        validate_notes(path, data)
        by_date[day] = data
    return by_date


def validate_coverage(scenario: str, data_by_date: dict[date, dict]) -> tuple[int, int]:
    effective_days = len(data_by_date)
    paired_dates = {day for day, data in data_by_date.items() if is_paired_day(data)}
    paired_days = len(paired_dates)
    expected_effective_days = SCENARIOS[scenario]["expected_effective_days"]
    expected_paired_days = SCENARIOS[scenario]["expected_paired_days"]
    expected_paired_dates = SCENARIOS[scenario]["expected_paired_dates"]

    if effective_days != expected_effective_days:
        raise ValueError(
            f"{scenario}: effective days must be {expected_effective_days}, got {effective_days}"
        )
    if paired_days != expected_paired_days:
        raise ValueError(f"{scenario}: paired days must be {expected_paired_days}, got {paired_days}")
    if paired_dates != expected_paired_dates:
        expected = ", ".join(day.isoformat() for day in sorted(expected_paired_dates))
        actual = ", ".join(day.isoformat() for day in sorted(paired_dates))
        raise ValueError(f"{scenario}: expected paired dates [{expected}], got [{actual}]")
    return effective_days, paired_days


def section_after_heading(text: str, heading: str) -> str:
    marker = f"\n{heading}\n"
    if marker not in text:
        raise ValueError(f"report missing {heading}")
    section = text.split(marker, 1)[1]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    return section.strip()


def subsection_after_heading(section: str, heading: str) -> str:
    text = f"\n{section.strip()}\n"
    marker = f"\n{heading}\n"
    if marker not in text:
        raise ValueError(f"C8 section missing {heading}")
    subsection = text.split(marker, 1)[1]
    next_heading = subsection.find("\n### ")
    if next_heading != -1:
        subsection = subsection[:next_heading]
    return subsection.strip()


def c8_subsections(section: str) -> dict[str, str]:
    return {
        "conclusion": subsection_after_heading(section, "### 结论"),
        "evidence": subsection_after_heading(section, "### 依据"),
        "boundary": subsection_after_heading(section, "### 边界"),
    }


def validate_report_set(scenario: str) -> dict[str, str]:
    root = scenario_report_root(scenario)
    files = sorted(path.name for path in root.glob("*.md"))
    expected = sorted(EXPECTED_REPORTS)
    if files != expected:
        raise ValueError(f"{scenario}: expected reports {expected}, got {files}")

    reports: dict[str, str] = {}
    for filename, report_path in EXPECTED_REPORTS.items():
        path = root / filename
        text = path.read_text(encoding="utf-8")
        if report_path not in text:
            raise ValueError(f"{path}: missing report path {report_path}")
        coverage_key = "weekly_coverage" if filename.startswith("weekly-") else "monthly_coverage"
        coverage = SCENARIOS[scenario][coverage_key]
        if coverage not in text:
            raise ValueError(f"{path}: missing coverage line {coverage}")
        section_after_heading(text, "## 跨维度观察")
        reports[filename] = text
    return reports


def source_backed_metric_snippets(data_by_date: dict[date, dict], paired_dates: set[date]) -> tuple[str, ...]:
    paired_data = [data_by_date[day] for day in sorted(paired_dates)]
    calories = [data["nutrition"]["total_calories"] for data in paired_data]
    protein = [data["nutrition"]["protein_g"] for data in paired_data]
    weights = [data["weight"]["value"] for data in paired_data]
    burns = [data["exercise"]["total_burn"] for data in paired_data]
    sleep_hours = [data["sleep"]["duration_h"] for data in paired_data]
    activity_count = sum(len(data["exercise"]["activities"]) for data in paired_data)

    return (
        f"热量范围 {format_range(calories)} kcal",
        f"蛋白质范围 {format_range(protein)} g",
        f"体重范围 {format_range(weights)} kg",
        f"运动/消耗范围 {format_range(burns)} kcal",
        f"活动次数 {activity_count} 次",
        f"睡眠范围 {format_range(sleep_hours)} h",
    )


def validate_insufficient_report(path_label: str, section: str) -> None:
    parts = c8_subsections(section)
    conclusion_lines = [line.strip() for line in parts["conclusion"].splitlines() if line.strip()]
    if conclusion_lines != [INSUFFICIENT_SENTENCE]:
        raise ValueError(f"{path_label}: insufficient conclusion must only contain the fixed sentence")
    for snippet in ("有效 JSON 天数：2", "候选关联配对日：1", "nutrition / weight"):
        if snippet not in parts["evidence"]:
            raise ValueError(f"{path_label}: insufficient evidence missing {snippet!r}")
    if INSUFFICIENT_SENTENCE not in parts["conclusion"]:
        raise ValueError(f"{path_label}: missing fixed insufficient-data sentence")
    conclusion_remainder = parts["conclusion"].replace(INSUFFICIENT_SENTENCE, "")
    for term in LOW_STRENGTH_TERMS + FORBIDDEN_MISSING_DATA_TERMS + FORBIDDEN_UNPROVIDED_DIMENSIONS:
        if term in conclusion_remainder:
            raise ValueError(f"{path_label}: insufficient conclusion must not include extra {term!r}")
    for term in FORBIDDEN_STRONG_TERMS + FORBIDDEN_UNPROVIDED_DIMENSIONS:
        if term in parts["evidence"]:
            raise ValueError(f"{path_label}: insufficient evidence must not include {term!r}")
    if not parts["boundary"]:
        raise ValueError(f"{path_label}: missing insufficient boundary text")


def validate_sufficient_report(path_label: str, section: str, metric_snippets: tuple[str, ...]) -> None:
    parts = c8_subsections(section)
    observation_text = f"{parts['conclusion']}\n{parts['evidence']}"
    if not any(term in parts["conclusion"] for term in LOW_STRENGTH_TERMS):
        raise ValueError(f"{path_label}: sufficient report needs low-strength observation wording")
    for snippet in ("3 个有效 JSON 天数", "3 个配对日"):
        if snippet not in observation_text:
            raise ValueError(f"{path_label}: missing {snippet}")
    for metric in REQUIRED_METRICS:
        if metric not in observation_text:
            raise ValueError(f"{path_label}: missing metric {metric}")
    for snippet in metric_snippets:
        if snippet not in parts["evidence"]:
            raise ValueError(f"{path_label}: missing source-backed metric {snippet!r}")
    for term in FORBIDDEN_STRONG_TERMS:
        if term in observation_text:
            raise ValueError(f"{path_label}: sufficient report must not include {term!r}")
    for term in FORBIDDEN_UNPROVIDED_DIMENSIONS:
        if term in observation_text:
            raise ValueError(f"{path_label}: sufficient report must not mention {term!r}")
    if not parts["boundary"]:
        raise ValueError(f"{path_label}: missing sufficient boundary text")


def validate_scenario(scenario: str) -> tuple[int, int]:
    data_by_date = load_scenario_json(scenario)
    effective_days, paired_days = validate_coverage(scenario, data_by_date)
    paired_dates = SCENARIOS[scenario]["expected_paired_dates"]
    reports = validate_report_set(scenario)
    metric_snippets = source_backed_metric_snippets(data_by_date, paired_dates) if scenario == "sufficient" else ()

    for filename, text in reports.items():
        path_label = f"{scenario}/{filename}"
        section = section_after_heading(text, "## 跨维度观察")
        if scenario == "sufficient":
            validate_sufficient_report(path_label, section, metric_snippets)
        else:
            validate_insufficient_report(path_label, section)
    return effective_days, paired_days


def main() -> int:
    actual_scenarios = sorted(path.name for path in FIXTURE_ROOT.iterdir() if path.is_dir())
    expected_scenarios = sorted(SCENARIOS)
    if actual_scenarios != expected_scenarios:
        raise ValueError(f"expected scenarios {expected_scenarios}, got {actual_scenarios}")

    for scenario in expected_scenarios:
        effective_days, paired_days = validate_scenario(scenario)
        print(f"{scenario}: effective days {effective_days}, paired days {paired_days}")
    print("validated Phase 3A C8 synthetic fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
