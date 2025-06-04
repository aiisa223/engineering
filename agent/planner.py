"""Planning module for the engineering agent."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    description: str
    priority: int


class Planner:
    """Heuristically decomposes a goal into actionable tasks."""

    def plan(self, goal: str, _depth: int = 0) -> List[Task]:
        if not goal:
            return []

        segments = [seg.strip() for seg in re.split(r"[.;]", goal) if seg.strip()]
        tasks: List[Task] = []
        priority = 10 - _depth

        for seg in segments:
            tasks.append(Task(description=seg, priority=priority))

            # recursively expand certain keywords
            lower = seg.lower()
            if _depth < 2 and ("design" in lower or "specification" in lower):
                tasks.extend(self.plan("Create simulation model", _depth + 1))
                tasks.extend(self.plan("Verify requirements", _depth + 1))

        if _depth == 0 and "nuclear" in goal.lower() and "reactor" in goal.lower():
            extras = [
                "Define safety goals",
                "Draft thermal system specification",
                "Calculate core size and materials",
                "Simulate coolant flow",
                "Run heat dispersion simulation",
            ]
            for ext in extras:
                tasks.extend(self.plan(ext, 1))

        # Remove duplicates while preserving order
        seen = set()
        unique: List[Task] = []
        for t in tasks:
            if t.description not in seen:
                seen.add(t.description)
                unique.append(t)

        return unique
