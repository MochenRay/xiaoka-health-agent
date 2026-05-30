#!/usr/bin/env python3
"""Generate a non-executing OpenClaw runtime smoke plan for Xiaoka.

This script is intentionally dry-run only. It reads a jobs.json-like file and
prints the backup, injection, run-history, and restore steps that a maintainer
must review before running any real OpenClaw cron job.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


XIAOKA_JOB_NAMES = ("零点结算", "结算校验", "前日汇总", "周报", "月报")
RUNTIME_JOB_PATH = "~/.openclaw/cron/jobs.json"
STANDARD_RUNTIME_PATHS = (
    "config/profile.md",
    "config/goals.md",
    "workspace/logs/",
    "workspace/data/",
    "workspace/reports/",
)


@dataclass(frozen=True)
class SmokeJob:
    name: str
    job_id: str
    enabled: bool
    delivery_mode: str
    schedule: dict[str, Any]

    @property
    def requires_announce_confirmation(self) -> bool:
        return self.delivery_mode == "announce"


def load_jobs(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        jobs = data
    elif isinstance(data, dict):
        jobs = data.get("jobs", [])
    else:
        raise ValueError(f"{path}: expected list or object with jobs")
    if not isinstance(jobs, list):
        raise ValueError(f"{path}: jobs must be a list")
    return [job for job in jobs if isinstance(job, dict)]


def select_xiaoka_jobs(jobs: list[dict[str, Any]]) -> list[SmokeJob]:
    selected: list[SmokeJob] = []
    for expected_name in XIAOKA_JOB_NAMES:
        matches = [
            job
            for job in jobs
            if job.get("name") == expected_name
            and isinstance(job.get("delivery"), dict)
            and job["delivery"].get("accountId") == "xiaoka"
        ]
        if len(matches) != 1:
            raise ValueError(f"expected exactly one xiaoka job named {expected_name}, got {len(matches)}")
        job = matches[0]
        job_id = job.get("id")
        if not isinstance(job_id, str) or not job_id:
            raise ValueError(f"{expected_name}: missing job id")
        delivery_mode = job["delivery"].get("mode")
        if delivery_mode not in {"none", "announce"}:
            raise ValueError(f"{expected_name}: unexpected delivery mode {delivery_mode!r}")
        schedule = job.get("schedule")
        if not isinstance(schedule, dict):
            raise ValueError(f"{expected_name}: missing schedule")
        selected.append(
            SmokeJob(
                name=expected_name,
                job_id=job_id,
                enabled=bool(job.get("enabled")),
                delivery_mode=delivery_mode,
                schedule=schedule,
            )
        )
    return selected


def build_plan(jobs: list[SmokeJob], workspace_root: str, scenario: str) -> dict[str, Any]:
    if scenario not in {"report", "c8", "deep-analysis", "google-health-import"}:
        raise ValueError(f"unsupported scenario {scenario!r}")

    announce_jobs = [job.name for job in jobs if job.requires_announce_confirmation]
    return {
        "mode": "dry-run-plan-only",
        "scenario": scenario,
        "workspace_root": workspace_root,
        "runtime_jobs_path": RUNTIME_JOB_PATH,
        "selected_jobs": [
            {
                "name": job.name,
                "id": job.job_id,
                "enabled": job.enabled,
                "delivery_mode": job.delivery_mode,
                "schedule": job.schedule,
                "requires_announce_confirmation": job.requires_announce_confirmation,
            }
            for job in jobs
        ],
        "guardrails": [
            "Do not run openclaw cron run from this planner.",
            "Back up ~/.openclaw/cron/jobs.json before any runtime edit.",
            "Back up target workspace/data and workspace/reports files before injection.",
            "Confirm recipient and test window before any announce delivery.",
            "Do not commit personal health data, OAuth tokens, raw API responses, or Telegram targets.",
            "After any manual run, inspect final run history; queued is not success.",
        ],
        "standard_runtime_paths": list(STANDARD_RUNTIME_PATHS),
        "requires_user_confirmation_before_real_run": bool(announce_jobs),
        "announce_jobs": announce_jobs,
        "manual_steps": [
            f"Back up {RUNTIME_JOB_PATH}.",
            f"Back up affected files under {workspace_root}/workspace/data and {workspace_root}/workspace/reports.",
            "Inject only synthetic or user-approved short-window data into ignored workspace paths.",
            "If a real run is approved, run the specific job with openclaw cron run <id> --wait --expect-final.",
            "Inspect openclaw cron runs for the final status and response.",
            "Archive generated reports, remove synthetic injected data, and restore original files.",
            "Record what was run without secrets, chat IDs, or personal health details.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs-json", required=True, help="Path to an OpenClaw jobs.json or synthetic fixture")
    parser.add_argument("--workspace-root", default="~/.openclaw/workspace-xiaoka")
    parser.add_argument(
        "--scenario",
        default="report",
        choices=("report", "c8", "deep-analysis", "google-health-import"),
    )
    args = parser.parse_args()

    jobs = select_xiaoka_jobs(load_jobs(Path(args.jobs_json)))
    plan = build_plan(jobs, args.workspace_root, args.scenario)
    print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
