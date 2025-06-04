"""Simple critique system for task results."""

from __future__ import annotations


class CritiqueEngine:
    def critique(self, output: str) -> str:
        if not output:
            return "No output produced."
        remarks = []
        out_lower = output.lower()
        if "error" in out_lower:
            remarks.append("contains error")
        if "warning" in out_lower:
            remarks.append("issued warning")
        if "0" in output:
            remarks.append("result may be zero")
        if not remarks:
            return "Looks reasonable"
        return "; ".join(remarks)
