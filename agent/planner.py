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

    def plan(self, goal: str) -> List[Task]:
        if not goal:
            return []

        # Split the goal into coarse segments using punctuation
        segments = re.split(r"[.;]", goal)
        tasks = [seg.strip() for seg in segments if seg.strip()]

        # Provide additional standard engineering steps when certain keywords
        # are present.
        g = goal.lower()
        if "nuclear" in g and "reactor" in g:
            extras = [
                "Define safety goals",
                "Draft thermal system specification",
                "Calculate core size and materials",
                "Simulate coolant flow",
                "Run heat dispersion simulation",
            ]
            tasks.extend(extras)

        # Remove duplicates while preserving order
        seen = set()
        unique_tasks: List[Task] = []
        priority = len(tasks)
        for t in tasks:
            if t not in seen:
                unique_tasks.append(Task(description=t, priority=priority))
                seen.add(t)
                priority -= 1
        return unique_tasks
