#!/usr/bin/env python3
"""Normalize Google Health API fixture data into Xiaoka log records.

This v1 importer is deliberately repo-layer only: it never performs OAuth or
network access. Pass a redacted fixture with --fixture-input, inspect records
with --dry-run, and use --apply only to append normalized rows to workspace logs.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IMPORT_MARKER = "xiaoka-google-health-api-importer:v1"
IMPORT_SECTION = "## Google Health API 导入"
TABLE_HEADER = "| record_id | 日期 | 类型 | 来源 | interval | 值 | 备注 |"
TABLE_DIVIDER = "|-----------|------|------|------|----------|----|------|"
REDACTED = "[REDACTED]"
SENSITIVE_KEY_TOKENS = (
    "authorization",
    "accesstoken",
    "refreshtoken",
    "clientsecret",
    "healthuserid",
    "legacyuserid",
    "rawresponse",
    "email",
)
SENSITIVE_TEXT_PATTERNS = (
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
)
FORBIDDEN_OUTPUT_TOKENS = (
    "access_token",
    "refreshtoken",
    "refresh_token",
    "client_secret",
    "authorization",
    "healthuserid",
    "healthUserId",
    "legacyuserid",
    "legacyUserId",
    "raw_response",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def sensitive_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", key.lower())
    return any(token in normalized for token in SENSITIVE_KEY_TOKENS)


def redact_sensitive(value: Any) -> Any:
    """Return a copy with known OAuth/account/raw-response fields redacted."""

    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if sensitive_key(str(key)):
                redacted[key] = REDACTED
            else:
                redacted[key] = redact_sensitive(item)
        return redacted
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, str):
        actual = value
        for pattern in SENSITIVE_TEXT_PATTERNS:
            actual = pattern.sub(REDACTED, actual)
        return actual
    return value


def assert_no_sensitive_payload(value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    compact = re.sub(r"[^a-zA-Z0-9_]", "", text)
    lowered = text.lower()
    compact_lowered = compact.lower()
    for token in FORBIDDEN_OUTPUT_TOKENS:
        if token.lower() in lowered or token.lower() in compact_lowered:
            raise ValueError(f"normalized output contains forbidden sensitive token {token!r}")
    for pattern in SENSITIVE_TEXT_PATTERNS:
        if pattern.search(text):
            raise ValueError("normalized output contains forbidden secret/account-like text")


def first_present(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def numeric_value(value: Any) -> float | int | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        return int(parsed) if parsed.is_integer() else parsed
    if isinstance(value, dict):
        for key in (
            "integerValue",
            "doubleValue",
            "intVal",
            "fpVal",
            "count",
            "value",
            "amount",
        ):
            parsed = numeric_value(value.get(key))
            if parsed is not None:
                return parsed
    if isinstance(value, list):
        total = 0.0
        found = False
        for item in value:
            parsed = numeric_value(item)
            if parsed is not None:
                total += float(parsed)
                found = True
        if found:
            return int(total) if total.is_integer() else total
    return None


def rounded(value: float | int | None, digits: int = 2) -> float | int | None:
    if value is None:
        return None
    actual = round(float(value), digits)
    return int(actual) if actual.is_integer() else actual


def millis_to_minutes(value: Any) -> float | int | None:
    parsed = numeric_value(value)
    if parsed is None:
        return None
    return rounded(float(parsed) / 60000, 1)


def millis_to_hours(value: Any) -> float | int | None:
    parsed = numeric_value(value)
    if parsed is None:
        return None
    return rounded(float(parsed) / 3600000, 2)


def meters_to_km(value: Any) -> float | int | None:
    parsed = numeric_value(value)
    if parsed is None:
        return None
    return rounded(float(parsed) / 1000, 2)


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def date_from_google_date(value: Any) -> str | None:
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value
    if isinstance(value, str) and len(value) >= 10:
        candidate = value[:10]
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", candidate):
            return candidate
    if isinstance(value, dict):
        year = numeric_value(value.get("year"))
        month = numeric_value(value.get("month"))
        day = numeric_value(value.get("day"))
        if year and month and day:
            return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return None


def date_from_datetime(value: str | None, prefer_end: bool = False) -> str | None:
    parsed = parse_datetime(value)
    if parsed is None:
        return None
    return parsed.date().isoformat()


def time_from_datetime(value: str | None) -> str | None:
    parsed = parse_datetime(value)
    if parsed is None:
        return None
    return parsed.strftime("%H:%M")


def interval_of(item: dict[str, Any]) -> tuple[str | None, str | None, str]:
    interval = item.get("interval") if isinstance(item.get("interval"), dict) else {}
    start = first_present(
        interval.get("startTime"),
        interval.get("civilStartTime"),
        interval.get("civil_start_time"),
        item.get("startTime"),
        item.get("start_time"),
    )
    end = first_present(
        interval.get("endTime"),
        interval.get("civilEndTime"),
        interval.get("civil_end_time"),
        item.get("endTime"),
        item.get("end_time"),
    )
    if start and end:
        return str(start), str(end), f"{start}/{end}"
    if start:
        return str(start), None, str(start)
    if end:
        return None, str(end), str(end)
    date_value = date_from_google_date(item.get("date"))
    return None, None, date_value or "unknown"


def source_details(*containers: dict[str, Any]) -> dict[str, str]:
    source_items: list[dict[str, Any]] = []
    for container in containers:
        for key in ("sources", "dataSources", "data_sources"):
            values = container.get(key)
            if isinstance(values, list):
                source_items.extend(item for item in values if isinstance(item, dict))
        value = container.get("source")
        if isinstance(value, dict):
            source_items.append(value)

    source = source_items[0] if source_items else {}
    device = source.get("device") if isinstance(source.get("device"), dict) else {}
    platform = first_present(source.get("platform"), source.get("sourcePlatform"), source.get("source_platform"))
    application = first_present(
        source.get("application"),
        source.get("applicationId"),
        source.get("packageName"),
        source.get("appPackageName"),
    )
    form_factor = first_present(
        device.get("formFactor"),
        source.get("deviceFormFactor"),
        source.get("sourceDeviceFormFactor"),
    )

    result = {
        "source": "google_health_api_healthkit" if platform == "HEALTH_KIT" else "google_health_api",
    }
    if platform:
        result["source_platform"] = str(platform)
    if application:
        result["source_application"] = str(application)
    if form_factor:
        result["source_device_form_factor"] = str(form_factor)
    return result


def list_items(container: Any, names: tuple[str, ...]) -> list[dict[str, Any]]:
    if isinstance(container, list):
        return [item for item in container if isinstance(item, dict)]
    if not isinstance(container, dict):
        return []
    for name in names:
        values = container.get(name)
        if isinstance(values, list):
            return [item for item in values if isinstance(item, dict)]
    if any(key in container for key in ("date", "interval", "value", "sleep", "exercise")):
        return [container]
    return []


def record_id(record: dict[str, Any]) -> str:
    key = {
        "date": record.get("date"),
        "kind": record.get("kind"),
        "source": record.get("source"),
        "interval": record.get("interval"),
    }
    digest = hashlib.sha256(json.dumps(key, sort_keys=True).encode("utf-8")).hexdigest()
    return digest[:12]


def finalize_record(record: dict[str, Any]) -> dict[str, Any]:
    clean = {key: value for key, value in record.items() if value is not None}
    clean["record_id"] = record_id(clean)
    clean.setdefault("confidence", "high")
    assert_no_sensitive_payload(clean)
    return clean


def normalize_steps(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    container = first_present(fixture.get("steps_daily_rollup"), fixture.get("stepsDailyRollUp"), {})
    items = list_items(container, ("dailyRollUp", "daily_rollup", "dailyMetrics", "points", "dataPoints"))
    records: list[dict[str, Any]] = []
    for item in items:
        start, end, interval = interval_of(item)
        count = numeric_value(first_present(item.get("count"), item.get("value"), item.get("values")))
        if count is None:
            continue
        date_value = first_present(
            date_from_google_date(item.get("date")),
            date_from_google_date(item.get("civilDate")),
            date_from_datetime(start),
        )
        if not date_value:
            raise ValueError("steps daily rollup item is missing a date")
        record = {
            "date": date_value,
            "kind": "steps",
            "interval": interval,
            "count": int(count),
            **source_details(container if isinstance(container, dict) else {}, item),
        }
        records.append(finalize_record(record))
    return records


def normalize_sleep(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    container = first_present(fixture.get("sleep_data_points"), fixture.get("sleepDataPoints"), {})
    items = list_items(container, ("dataPoints", "data_points", "points"))
    records: list[dict[str, Any]] = []
    for item in items:
        payload = item.get("sleep") if isinstance(item.get("sleep"), dict) else item
        start, end, interval = interval_of(item)
        duration_h = first_present(
            numeric_value(payload.get("durationHours")),
            numeric_value(payload.get("duration_h")),
            millis_to_hours(payload.get("durationMillis")),
        )
        time_in_bed_h = first_present(
            numeric_value(payload.get("timeInBedHours")),
            numeric_value(payload.get("time_in_bed_h")),
            millis_to_hours(payload.get("timeInBedMillis")),
        )
        if duration_h is None and start and end:
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(end)
            if start_dt and end_dt:
                duration_h = rounded((end_dt - start_dt).total_seconds() / 3600, 2)
        stages = payload.get("stages") if isinstance(payload.get("stages"), dict) else {}
        stage_map = {
            "awake_min": first_present(stages.get("awake_min"), stages.get("awakeMinutes")),
            "rem_min": first_present(stages.get("rem_min"), stages.get("remMinutes")),
            "core_min": first_present(stages.get("core_min"), stages.get("coreMinutes")),
            "deep_min": first_present(stages.get("deep_min"), stages.get("deepMinutes")),
        }
        normalized_stages = {
            key: numeric_value(value) for key, value in stage_map.items() if numeric_value(value) is not None
        }
        efficiency = first_present(
            numeric_value(payload.get("efficiencyPercent")),
            numeric_value(payload.get("efficiency_pct")),
        )
        if efficiency is None and duration_h and time_in_bed_h:
            efficiency = rounded(float(duration_h) / float(time_in_bed_h) * 100, 0)
        date_value = first_present(
            date_from_google_date(item.get("date")),
            date_from_google_date(payload.get("date")),
            date_from_datetime(end),
            date_from_datetime(start),
        )
        if not date_value:
            raise ValueError("sleep data point is missing a date or interval")
        record = {
            "date": date_value,
            "kind": "sleep",
            "interval": interval,
            "duration_h": rounded(duration_h, 2) if duration_h is not None else None,
            "time_in_bed_h": rounded(time_in_bed_h, 2) if time_in_bed_h is not None else None,
            "efficiency_pct": rounded(efficiency, 0) if efficiency is not None else None,
            "start_time": time_from_datetime(start),
            "end_time": time_from_datetime(end),
            "quality": payload.get("quality"),
            "stages": normalized_stages or None,
            **source_details(container if isinstance(container, dict) else {}, item),
        }
        records.append(finalize_record(record))
    return records


def normalize_exercise(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    container = first_present(fixture.get("exercise_data_points"), fixture.get("exerciseDataPoints"), {})
    items = list_items(container, ("dataPoints", "data_points", "points"))
    records: list[dict[str, Any]] = []
    for item in items:
        payload = item.get("exercise") if isinstance(item.get("exercise"), dict) else item
        start, end, interval = interval_of(item)
        duration_min = first_present(
            numeric_value(payload.get("durationMinutes")),
            numeric_value(payload.get("duration_min")),
            millis_to_minutes(payload.get("durationMillis")),
        )
        if duration_min is None and start and end:
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(end)
            if start_dt and end_dt:
                duration_min = rounded((end_dt - start_dt).total_seconds() / 60, 1)
        distance_km = first_present(
            numeric_value(payload.get("distanceKm")),
            numeric_value(payload.get("distance_km")),
            meters_to_km(payload.get("distanceMeters")),
        )
        date_value = first_present(
            date_from_google_date(item.get("date")),
            date_from_google_date(payload.get("date")),
            date_from_datetime(start),
            date_from_datetime(end),
        )
        if not date_value:
            raise ValueError("exercise data point is missing a date or interval")
        record = {
            "date": date_value,
            "kind": "exercise",
            "interval": interval,
            "type": first_present(payload.get("activityType"), payload.get("type"), "exercise"),
            "duration_min": rounded(duration_min, 1) if duration_min is not None else None,
            "active_energy_kcal": numeric_value(
                first_present(payload.get("activeEnergyKcal"), payload.get("active_energy_kcal"))
            ),
            "distance_km": rounded(distance_km, 2) if distance_km is not None else None,
            "steps": numeric_value(payload.get("steps")),
            "start_time": time_from_datetime(start),
            "end_time": time_from_datetime(end),
            **source_details(container if isinstance(container, dict) else {}, item),
        }
        records.append(finalize_record(record))
    return records


def normalize_google_health_fixture(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    redacted = redact_sensitive(fixture)
    records = normalize_steps(redacted)
    records.extend(normalize_sleep(redacted))
    records.extend(normalize_exercise(redacted))
    records.sort(key=lambda item: (item["date"], item["kind"], item["interval"]))
    assert_no_sensitive_payload(records)
    return records


def markdown_cell(value: Any) -> str:
    if value is None:
        return "null"
    return str(value).replace("\n", " ").replace("|", "/").strip()


def record_value(record: dict[str, Any]) -> str:
    kind = record["kind"]
    if kind == "steps":
        return f"{record['count']} steps"
    if kind == "sleep":
        parts = [f"{record.get('duration_h')}h"]
        if record.get("time_in_bed_h") is not None:
            parts.append(f"time_in_bed {record['time_in_bed_h']}h")
        if record.get("efficiency_pct") is not None:
            parts.append(f"efficiency {record['efficiency_pct']}%")
        return "; ".join(parts)
    if kind == "exercise":
        parts = [str(record.get("type", "exercise"))]
        if record.get("duration_min") is not None:
            parts.append(f"{record['duration_min']} min")
        if record.get("active_energy_kcal") is not None:
            parts.append(f"{record['active_energy_kcal']} kcal")
        if record.get("distance_km") is not None:
            parts.append(f"{record['distance_km']} km")
        if record.get("steps") is not None:
            parts.append(f"{record['steps']} steps")
        return "; ".join(parts)
    return json.dumps(record, ensure_ascii=False, sort_keys=True)


def record_note(record: dict[str, Any]) -> str:
    parts = [IMPORT_MARKER]
    for key, label in (
        ("start_time", "start"),
        ("end_time", "end"),
        ("source_platform", "source_platform"),
        ("source_application", "source_application"),
        ("source_device_form_factor", "device"),
        ("confidence", "confidence"),
    ):
        if record.get(key) is not None:
            parts.append(f"{label} {record[key]}")
    stages = record.get("stages")
    if isinstance(stages, dict) and stages:
        stage_text = ", ".join(f"{key} {value}min" for key, value in sorted(stages.items()))
        parts.append(f"stages {stage_text}")
    return "; ".join(parts)


def record_row(record: dict[str, Any]) -> str:
    cells = [
        record["record_id"],
        record["date"],
        record["kind"],
        record["source"],
        record["interval"],
        record_value(record),
        record_note(record),
    ]
    row = "| " + " | ".join(markdown_cell(cell) for cell in cells) + " |"
    assert_no_sensitive_payload(row)
    return row


def default_log(date_value: str) -> str:
    return f"""# {date_value} 健康日志

## 体重
<!-- 未记录 -->

## 饮食
<!-- 未记录 -->

## 运动
<!-- 未记录 -->

## 补剂
<!-- 未记录 -->

## 睡眠
<!-- 未记录 -->

## 备注
<!-- 用户或小卡的额外备注 -->
"""


def ensure_import_section(text: str) -> str:
    if IMPORT_SECTION not in text:
        block = f"\n{IMPORT_SECTION}\n<!-- {IMPORT_MARKER} -->\n\n{TABLE_HEADER}\n{TABLE_DIVIDER}\n"
        marker = "\n## 备注"
        if marker in text:
            return text.replace(marker, block + marker, 1)
        return text.rstrip() + block + "\n"
    if f"<!-- {IMPORT_MARKER} -->" not in text:
        text = text.replace(IMPORT_SECTION, f"{IMPORT_SECTION}\n<!-- {IMPORT_MARKER} -->", 1)
    if TABLE_HEADER not in text:
        text = text.replace(
            f"<!-- {IMPORT_MARKER} -->",
            f"<!-- {IMPORT_MARKER} -->\n\n{TABLE_HEADER}\n{TABLE_DIVIDER}",
            1,
        )
    return text


def append_row(text: str, row: str) -> tuple[str, bool]:
    record = row.split("|", 3)[1].strip()
    if f"| {record} |" in text:
        return text, False
    text = ensure_import_section(text)
    start = text.index(IMPORT_SECTION)
    next_section = text.find("\n## ", start + len(IMPORT_SECTION))
    insert_at = len(text) if next_section == -1 else next_section + 1
    prefix = text[:insert_at].rstrip()
    suffix = text[insert_at:] if next_section != -1 else ""
    return f"{prefix}\n{row}\n{suffix}", True


def log_path_for(workspace_root: Path, date_value: str) -> Path:
    month, day = date_value[:7], date_value[8:10]
    return workspace_root / "logs" / month / f"{day}.md"


def append_records_to_workspace(records: list[dict[str, Any]], workspace_root: Path) -> dict[str, Any]:
    by_date: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_date.setdefault(record["date"], []).append(record)

    summary = {"added": 0, "skipped": 0, "files": []}
    for date_value, date_records in sorted(by_date.items()):
        path = log_path_for(workspace_root, date_value)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8") if path.exists() else default_log(date_value)
        file_added = 0
        file_skipped = 0
        for record in date_records:
            row = record_row(record)
            text, added = append_row(text, row)
            if added:
                file_added += 1
            else:
                file_skipped += 1
        assert_no_sensitive_payload(text)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        summary["added"] += file_added
        summary["skipped"] += file_skipped
        summary["files"].append(
            {
                "path": path.as_posix(),
                "added": file_added,
                "skipped": file_skipped,
            }
        )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-input",
        type=Path,
        help="Path to a redacted Google Health API fixture JSON file.",
    )
    parser.add_argument(
        "--date",
        help="Optional YYYY-MM-DD filter for normalized records.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print normalized records without writing workspace logs.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Append normalized records to workspace/logs/YYYY-MM/DD.md.",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=ROOT / "workspace",
        help="Workspace root used with --apply. Default: repo workspace/.",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.apply and args.dry_run:
        parser.error("--apply and --dry-run are mutually exclusive")
    if args.fixture_input is None:
        print(
            "Google Health OAuth/network import is intentionally not implemented in repo v1; "
            "pass --fixture-input with a redacted fixture. No network attempted.",
            file=sys.stderr,
        )
        return 2
    fixture = load_json(args.fixture_input)
    records = normalize_google_health_fixture(fixture)
    if args.date:
        records = [record for record in records if record["date"] == args.date]
    if args.apply:
        summary = append_records_to_workspace(copy.deepcopy(records), args.workspace_root)
        print(json.dumps({"records": len(records), **summary}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"records": records}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
