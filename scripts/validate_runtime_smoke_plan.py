#!/usr/bin/env python3
"""Validate the dry-run OpenClaw runtime smoke planner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNER_PATH = ROOT / "scripts" / "plan_runtime_smoke.py"
FIXTURE_PATH = ROOT / "fixtures" / "synthetic" / "runtime-smoke" / "openclaw-jobs.json"


def load_planner():
    spec = importlib.util.spec_from_file_location("plan_runtime_smoke", PLANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load plan_runtime_smoke.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    planner = load_planner()
    jobs = planner.select_xiaoka_jobs(planner.load_jobs(FIXTURE_PATH))
    assert_true([job.name for job in jobs] == list(planner.XIAOKA_JOB_NAMES), "xiaoka job order mismatch")
    assert_true(len([job for job in jobs if job.delivery_mode == "announce"]) == 3, "announce job count mismatch")

    plan = planner.build_plan(jobs, "~/.openclaw/workspace-xiaoka", "c8")
    assert_true(plan["mode"] == "dry-run-plan-only", "planner must remain dry-run only")
    assert_true(plan["requires_user_confirmation_before_real_run"], "announce jobs must require confirmation")
    assert_true("周报" in plan["announce_jobs"], "weekly report should be announce-gated")
    assert_true("月报" in plan["announce_jobs"], "monthly report should be announce-gated")
    assert_true(any("Do not run openclaw cron run" in item for item in plan["guardrails"]), "missing run ban")
    assert_true("workspace/data/" in plan["standard_runtime_paths"], "missing standard data path")

    result = subprocess.run(
        [
            sys.executable,
            str(PLANNER_PATH),
            "--jobs-json",
            str(FIXTURE_PATH),
            "--scenario",
            "google-health-import",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    cli_plan = json.loads(result.stdout)
    assert_true(cli_plan["scenario"] == "google-health-import", "CLI scenario mismatch")
    assert_true(len(cli_plan["selected_jobs"]) == 5, "CLI selected job count mismatch")
    assert_true("openclaw cron run <id> --wait --expect-final" in "\n".join(cli_plan["manual_steps"]), "missing final-run inspection step")

    print("runtime smoke planner validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
