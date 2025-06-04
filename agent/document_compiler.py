"""Compile a Markdown engineering report."""

from __future__ import annotations

import datetime
from typing import Iterable, List

try:
    from pylatex import Document, NoEscape
    _HAS_PYLATEX = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_PYLATEX = False


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

    def to_pdf(self, path: str, markdown: str) -> None:
        if not _HAS_PYLATEX:
            raise RuntimeError("pylatex not installed")
        doc = Document()
        for line in markdown.splitlines():
            if line.startswith("# "):
                doc.append(NoEscape(f"\\section*{{{line[2:]}}}"))
            elif line.startswith("## "):
                doc.append(NoEscape(f"\\subsection*{{{line[3:]}}}"))
            else:
                doc.append(NoEscape(line + "\\\n"))
        doc.generate_pdf(path, clean_tex=True)
