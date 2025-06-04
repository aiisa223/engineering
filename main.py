"""Entry point for the autonomous engineering agent."""

from __future__ import annotations

from agent.planner import Planner, Task
from agent.memory_manager import MemoryManager
from agent.reasoner import Reasoner
from agent.executor import Executor
from agent.critique_engine import CritiqueEngine
from agent.document_compiler import DocumentCompiler


def main() -> None:
    goal = "Design a modular nuclear reactor with passive safety systems, thermal output ≤ 100MW."

    planner = Planner()
    memory = MemoryManager()
    reasoner = Reasoner()
    executor = Executor()
    critique_engine = CritiqueEngine()
    compiler = DocumentCompiler()

    tasks = planner.plan(goal)
    results = []
    for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
        thought = reasoner.think(task.description)
        memory.remember(f"Thought: {thought}")

        code = reasoner.extract_code(thought)
        if code:
            exec_result = executor.execute(f"python:{code}")
            memory.remember(f"Execution: {exec_result}", long_term=True)
        result = executor.execute(task.description)
        memory.remember(f"Result: {result}", long_term=True)

        critique = critique_engine.critique(result)
        memory.remember(f"Critique: {critique}")

        results.append(f"{result} ({critique})")

    report = compiler.compile(goal, [t.description for t in tasks], results)
    print(report)
    compiler.write("report.md", report)
    try:
        compiler.to_pdf("report", report)
    except Exception:
        pass


if __name__ == "__main__":
    main()
