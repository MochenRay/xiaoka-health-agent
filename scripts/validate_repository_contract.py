#!/usr/bin/env python3
"""Validate repository-level contracts that are easy to drift."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILL_LINE_LIMIT = 200
REFERENCE_REQUIRED_KEYS = ("source", "last_verified", "accuracy_note")
LEGACY_RUNTIME_DIRS = ("logs/", "data/", "medical/", "reports/", "food-library/")
LEGACY_ALLOWED_CONTEXT = (
    "LEGACY",
    "旧",
    "legacy",
    "禁止",
    "废弃",
    "迁移",
    "根目录",
    "兼容",
    "历史",
    "不得",
    "不读",
    "不应",
    "不再",
    "保留",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_json_files(files: list[Path]) -> int:
    json_files = [path for path in files if path.suffix == ".json"]
    for path in json_files:
        with path.open(encoding="utf-8") as handle:
            json.load(handle)
    print(f"json files valid: {len(json_files)}")
    return len(json_files)


def markdown_link_target(raw_target: str) -> str | None:
    target = raw_target.strip().split()[0]
    if not target or target.startswith("#"):
        return None
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return None
    if parsed.scheme and parsed.scheme != "file":
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    path_part = unquote(target.split("#", 1)[0])
    return path_part or None


def validate_markdown_links(files: list[Path]) -> int:
    markdown_files = [path for path in files if path.suffix == ".md"]
    checked = 0
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = markdown_link_target(match.group(1))
            if target is None:
                continue
            checked += 1
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                raise ValueError(f"{relative(path)}: missing markdown link target {target!r}")
            try:
                target_path.relative_to(ROOT)
            except ValueError as exc:
                raise ValueError(
                    f"{relative(path)}: markdown link target escapes repo {target!r}"
                ) from exc
    print(f"markdown local links valid: {checked}")
    return checked


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{relative(path)}: missing YAML-like metadata frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError(f"{relative(path)}: metadata frontmatter is not closed") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def validate_reference_metadata(files: list[Path]) -> int:
    reference_files = [
        path
        for path in files
        if path.parent == ROOT / "references" and path.suffix == ".md"
    ]
    for path in reference_files:
        metadata = frontmatter(path)
        for key in REFERENCE_REQUIRED_KEYS:
            if not metadata.get(key):
                raise ValueError(f"{relative(path)}: metadata key {key!r} is required")
    print(f"reference metadata valid: {len(reference_files)}")
    return len(reference_files)


def validate_skill_line_count() -> int:
    path = ROOT / "SKILL.md"
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    if line_count > SKILL_LINE_LIMIT:
        raise ValueError(f"SKILL.md has {line_count} lines; limit is {SKILL_LINE_LIMIT}")
    print(f"SKILL.md line count valid: {line_count}/{SKILL_LINE_LIMIT}")
    return line_count


def line_has_legacy_runtime_path(line: str) -> bool:
    if "workspace/" in line:
        return False
    for legacy_dir in LEGACY_RUNTIME_DIRS:
        index = line.find(legacy_dir)
        while index != -1:
            prefix = line[max(0, index - len("workspace/")) : index]
            if prefix != "workspace/":
                return True
            index = line.find(legacy_dir, index + len(legacy_dir))
    return False


def validate_legacy_runtime_mentions(files: list[Path]) -> int:
    text_files = [
        path
        for path in files
        if path.suffix in {".md", ".py", ".gitignore"} or path.name in {"SKILL.md", "SOUL.md"}
    ]
    checked = 0
    for path in text_files:
        if relative(path) == "workspace/README.md":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not line_has_legacy_runtime_path(line):
                continue
            checked += 1
            context = "\n".join(lines[max(0, index - 6) : min(len(lines), index + 7)])
            if not any(term in context for term in LEGACY_ALLOWED_CONTEXT):
                raise ValueError(
                    f"{relative(path)}:{index + 1}: legacy runtime path needs explicit "
                    "compatibility/forbidden context"
                )
    print(f"legacy runtime mentions contextualized: {checked}")
    return checked


def main() -> int:
    files = tracked_files()
    validate_json_files(files)
    validate_markdown_links(files)
    validate_reference_metadata(files)
    validate_skill_line_count()
    validate_legacy_runtime_mentions(files)
    print("repository contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
