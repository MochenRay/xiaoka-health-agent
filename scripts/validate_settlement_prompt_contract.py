#!/usr/bin/env python3
"""Validate the synthetic settlement prompt regression contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "fixtures/synthetic/settlement-prompt/workspace/logs/2026-07/02.md"
EXPECTED_JSON_PATH = (
    ROOT / "fixtures/synthetic/settlement-prompt/expected/workspace/data/2026-07/02.json"
)
RUNTIME_DOC_PATH = ROOT / "docs/openclaw-runtime.md"
SCHEMA_DOC_PATH = ROOT / "docs/data-schema.md"

REQUIRED_RUNTIME_SNIPPETS = (
    "写入：`workspace/data/{YYYY-MM}/{DD}.json`",
    "按 `docs/data-schema.md` 生成结构化 JSON",
    "若源日志不存在或无用户记录：静默跳过，不创建 JSON",
)
REQUIRED_SCHEMA_SNIPPETS = (
    '"weight"',
    '"nutrition"',
    '"exercise"',
    '"sleep"',
    '"supplements"',
)
REQUIRED_LOG_SNIPPETS = (
    "SYNTHETIC_SETTLEMENT",
    "体重：101.2 kg",
    "| **小计** | | **246** | **16.6g** | **17.2g** | **12.1g** |",
    "| **小计** | | **620** | **45g** | **70g** | **18g** |",
    "| 2026-07-02 | strength | 45 | 260 | manual |",
    "creatine_5g",
    "| 2026-07-02 | 7.0 | 23:45 | 06:45 | manual | fair |",
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{relative(path)}: expected a JSON object")
    return data


def require_snippets(path: Path, snippets: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        raise ValueError(f"{relative(path)}: missing snippets: {', '.join(missing)}")


def require_value(data: dict[str, Any], dotted_path: str, expected: Any) -> None:
    current: Any = data
    for key in dotted_path.split("."):
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"{relative(EXPECTED_JSON_PATH)}: missing {dotted_path}")
        current = current[key]
    if current != expected:
        raise ValueError(
            f"{relative(EXPECTED_JSON_PATH)}: {dotted_path} expected {expected!r}, got {current!r}"
        )


def validate_expected_json() -> None:
    data = load_json(EXPECTED_JSON_PATH)
    for dotted_path, expected in (
        ("date", "2026-07-02"),
        ("weight.value", 101.2),
        ("nutrition.total_calories", 866),
        ("nutrition.protein_g", 61.6),
        ("nutrition.carbs_g", 87.2),
        ("nutrition.fat_g", 30.1),
        ("exercise.total_burn", 260),
        ("sleep.duration_h", 7),
    ):
        require_value(data, dotted_path, expected)

    meals = data.get("nutrition", {}).get("meals")
    if not isinstance(meals, list) or len(meals) != 2:
        raise ValueError(f"{relative(EXPECTED_JSON_PATH)}: nutrition.meals must contain 2 meals")
    supplements = data.get("supplements")
    if supplements != ["creatine_5g", "vitamin_d_2000iu"]:
        raise ValueError(f"{relative(EXPECTED_JSON_PATH)}: supplements mismatch")
    notes = data.get("notes")
    if not isinstance(notes, str) or "not real health data" not in notes:
        raise ValueError(f"{relative(EXPECTED_JSON_PATH)}: notes must mark non-real synthetic data")


def main() -> int:
    require_snippets(RUNTIME_DOC_PATH, REQUIRED_RUNTIME_SNIPPETS)
    require_snippets(SCHEMA_DOC_PATH, REQUIRED_SCHEMA_SNIPPETS)
    require_snippets(LOG_PATH, REQUIRED_LOG_SNIPPETS)
    validate_expected_json()
    print("settlement prompt contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
