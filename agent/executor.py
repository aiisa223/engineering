"""Task execution and simulation utilities."""

from __future__ import annotations

import math
import textwrap
from typing import Optional

import numpy as np


class Executor:
    """Executes tasks by running simple calculations or simulations."""

    def execute(self, task: str) -> str:
        t = task.lower()
        if "heat" in t:
            temp = self._heat_simulation()
            return f"Heat simulation average temperature: {temp:.2f}"
        if "area" in t and "circle" in t:
            radius = self._extract_number(t)
            if radius is not None:
                return f"Area of circle (r={radius}) = {math.pi * radius ** 2:.2f}"
        if t.startswith("python:" ):
            code = task[len("python:"):]
            return self._run_python(code)
        return f"Completed: {task}"

    # ------------------------------------------------------------------
    def _heat_simulation(self) -> float:
        """Very small finite difference heat diffusion example."""
        L = 1.0
        N = 20
        alpha = 0.01
        steps = 100
        dx = L / N
        dt = 0.1 * dx ** 2 / alpha
        u = np.zeros(N + 1)
        u[0] = 100  # boundary condition
        for _ in range(steps):
            u[1:-1] = u[1:-1] + alpha * dt / dx ** 2 * (
                u[2:] - 2 * u[1:-1] + u[:-2]
            )
        return float(np.mean(u))

    def _extract_number(self, text: str) -> Optional[float]:
        for token in text.split():
            try:
                return float(token)
            except ValueError:
                continue
        return None

    def _run_python(self, code: str) -> str:
        locals_dict: dict = {}
        try:
            exec(textwrap.dedent(code), {}, locals_dict)
            return str(locals_dict.get("result", "python executed"))
        except Exception as e:
            return f"error executing python: {e}"
