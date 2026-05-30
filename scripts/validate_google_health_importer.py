#!/usr/bin/env python3
"""Validate the repo-layer Google Health API importer with synthetic data."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMPORTER_PATH = ROOT / "scripts" / "import_google_health.py"
FIXTURE_PATH = ROOT / "fixtures" / "synthetic" / "google-health-api" / "google-health-api-synthetic.json"


def load_importer():
    spec = importlib.util.spec_from_file_location("import_google_health", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load importer from {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IMPORTER = load_importer()


class GoogleHealthImporterTests(unittest.TestCase):
    def load_fixture(self) -> dict:
        with FIXTURE_PATH.open(encoding="utf-8") as handle:
            return json.load(handle)

    def normalized_records(self) -> list[dict]:
        return IMPORTER.normalize_google_health_fixture(self.load_fixture())

    def test_normalize_synthetic_fixture(self) -> None:
        records = self.normalized_records()
        self.assertEqual(["exercise", "sleep", "steps"], sorted(record["kind"] for record in records))
        for record in records:
            self.assertEqual("2026-07-08", record["date"])
            self.assertEqual("google_health_api_healthkit", record["source"])
            self.assertEqual("HEALTH_KIT", record["source_platform"])
            self.assertIn(record["source_application"], {"com.apple.Health", "com.apple.Fitness"})
            self.assertRegex(record["record_id"], r"^[0-9a-f]{12}$")

        steps = next(record for record in records if record["kind"] == "steps")
        self.assertEqual(9824, steps["count"])
        sleep = next(record for record in records if record["kind"] == "sleep")
        self.assertEqual(7.43, sleep["duration_h"])
        self.assertEqual(93, sleep["efficiency_pct"])
        self.assertEqual(68, sleep["stages"]["deep_min"])
        exercise = next(record for record in records if record["kind"] == "exercise")
        self.assertEqual("outdoor_walk", exercise["type"])
        self.assertEqual(45, exercise["duration_min"])
        self.assertEqual(286, exercise["active_energy_kcal"])

    def test_redaction_keeps_allowed_source_fields(self) -> None:
        payload = {
            "Authorization": "Bearer synthetic-secret",
            "access_token": "synthetic-token",
            "nested": {
                "email": "synthetic@example.invalid",
                "healthUserId": "users/synthetic",
                "source_application": "com.apple.Health",
            },
        }
        redacted = IMPORTER.redact_sensitive(payload)
        self.assertEqual(IMPORTER.REDACTED, redacted["Authorization"])
        self.assertEqual(IMPORTER.REDACTED, redacted["access_token"])
        self.assertEqual(IMPORTER.REDACTED, redacted["nested"]["email"])
        self.assertEqual(IMPORTER.REDACTED, redacted["nested"]["healthUserId"])
        self.assertEqual("com.apple.Health", redacted["nested"]["source_application"])

    def test_idempotent_append(self) -> None:
        records = self.normalized_records()
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            first = IMPORTER.append_records_to_workspace(records, workspace_root)
            second = IMPORTER.append_records_to_workspace(records, workspace_root)
            self.assertEqual(len(records), first["added"])
            self.assertEqual(0, first["skipped"])
            self.assertEqual(0, second["added"])
            self.assertEqual(len(records), second["skipped"])

            log_path = workspace_root / "logs" / "2026-07" / "08.md"
            text = log_path.read_text(encoding="utf-8")
            self.assertIn("## Google Health API 导入", text)
            self.assertIn("xiaoka-google-health-api-importer:v1", text)
            for record in records:
                self.assertEqual(1, text.count(record["record_id"]))
            IMPORTER.assert_no_sensitive_payload(text)

    def test_no_secret_or_raw_response_persistence(self) -> None:
        records = self.normalized_records()
        serialized = json.dumps(records, ensure_ascii=False)
        for forbidden in ("dataPoints", "dailyRollUp", "raw_response", "Authorization"):
            self.assertNotIn(forbidden, serialized)
        IMPORTER.assert_no_sensitive_payload(records)

    def test_without_fixture_refuses_network_mode(self) -> None:
        result = subprocess.run(
            [sys.executable, str(IMPORTER_PATH), "--dry-run"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("No network attempted", result.stderr)
        self.assertEqual("", result.stdout)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GoogleHealthImporterTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print("validated Google Health API importer synthetic proof")
    print("covered: normalize, redaction, idempotent append, no secret/raw persistence, no-network default")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
