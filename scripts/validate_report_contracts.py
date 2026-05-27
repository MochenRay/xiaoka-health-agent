#!/usr/bin/env python3
"""Validate report automation and template contracts."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = {
    "docs/report-automation.md": (
        "workspace/data/",
        "workspace/logs/",
        "workspace/reports/",
        "NO_REPLY",
        "## 跨维度观察",
        "docs/c8-cross-dimensional-insights.md",
    ),
    "docs/c8-cross-dimensional-insights.md": (
        "workspace/data/YYYY-MM/DD.json",
        "## 跨维度观察",
        "### 结论",
        "### 依据",
        "### 边界",
    ),
    "docs/deep-analysis-report-contract.md": (
        "analysis_summaries",
        '"workflow": "M1"',
        "## M1 药物/补剂摘要",
        "## E1 运动摘要",
        "## S1 睡眠摘要",
        "本周没有新的 M1 结构化摘要；不做药物效果、依从性或剂量判断。",
        "运动记录不足 3 天，仅保留本周记录，不做训练趋势判断。",
        "睡眠记录不足 3 天，仅保留当前观察，不做趋势判断。",
        "不构成诊断、处方或自行调整剂量建议",
    ),
    "templates/weekly-report.md": (
        "workspace/reports/weekly-",
        "## 跨维度观察",
        "## 深度分析摘要",
        "### M1 药物/补剂",
        "### E1 运动",
        "### S1 睡眠",
        "### 结论",
        "### 依据",
        "### 边界",
    ),
    "templates/monthly-report.md": (
        "workspace/reports/monthly-",
        "## 跨维度观察",
        "## 深度分析摘要",
        "### M1 药物/补剂",
        "### E1 运动",
        "### S1 睡眠",
        "### 结论",
        "### 依据",
        "### 边界",
    ),
    "fixtures/synthetic/phase3b-deep-analysis/expected/weekly-report-sections.md": (
        "SYNTHETIC_PHASE3B expected wording",
        "## 深度分析摘要",
        "### M1 药物/补剂",
        "### E1 运动",
        "### S1 睡眠",
        "运动记录不足 3 天，仅保留本周记录，不做训练趋势判断。",
        "睡眠记录不足 3 天，仅保留当前观察，不做趋势判断。",
        "不做药物效果、依从性或剂量判断",
    ),
    "fixtures/synthetic/phase3b-deep-analysis/expected/monthly-report-sections.md": (
        "SYNTHETIC_PHASE3B expected wording",
        "## 深度分析摘要",
        "### M1 药物/补剂",
        "### E1 运动",
        "### S1 睡眠",
        "运动记录不足 3 天，仅保留本月记录，不做训练趋势判断。",
        "睡眠记录不足 3 天，仅保留当前观察，不做趋势判断。",
        "不做药物效果、依从性或剂量判断",
    ),
}
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
    "forbidden",
)
SECTION_RE = re.compile(r"^## 跨维度观察$", re.MULTILINE)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def validate_required_snippets(path: Path, text: str, snippets: tuple[str, ...]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        raise ValueError(f"{relative(path)}: missing required snippets: {', '.join(missing)}")
    if "templates/" in relative(path) and not SECTION_RE.search(text):
        raise ValueError(f"{relative(path)}: C8 section must use an exact level-2 heading")


def validate_legacy_runtime_context(path: Path, text: str) -> int:
    lines = text.splitlines()
    checked = 0
    for index, line in enumerate(lines):
        if not line_has_legacy_runtime_path(line):
            continue
        checked += 1
        context = "\n".join(lines[max(0, index - 6) : min(len(lines), index + 7)])
        if not any(term in context for term in LEGACY_ALLOWED_CONTEXT):
            raise ValueError(
                f"{relative(path)}:{index + 1}: legacy root runtime path needs explicit "
                "forbidden/compatibility context"
            )
    return checked


def main() -> int:
    legacy_mentions = 0
    for raw_path, snippets in CONTRACTS.items():
        path = ROOT / raw_path
        text = path.read_text(encoding="utf-8")
        validate_required_snippets(path, text, snippets)
        legacy_mentions += validate_legacy_runtime_context(path, text)
        print(f"report contract valid: {raw_path}")
    print(f"legacy root runtime mentions contextualized: {legacy_mentions}")
    print("report contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
