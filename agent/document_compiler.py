"""Compile a Markdown engineering report."""

from __future__ import annotations

import datetime
from typing import Iterable, List


class DocumentCompiler:
    def compile(self, goal: str, tasks: Iterable[str], results: Iterable[str]) -> str:
        lines = [f"# Project Report - {datetime.date.today()}", "", "## Goal", goal, "", "## Tasks"]
        lines.extend(f"- {t}" for t in tasks)
        lines.extend(["", "## Results"])
        lines.extend(f"- {r}" for r in results)
        return "\n".join(lines)

    def write(self, path: str, content: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
