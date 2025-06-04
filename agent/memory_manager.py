"""Memory management for the engineering agent."""

from __future__ import annotations

import json
import os
from collections import Counter
from typing import Dict, List, Tuple


class MemoryManager:
    """Stores short‑term and persistent long‑term memories."""

    def __init__(self, path: str = "memory.json") -> None:
        self.path = path
        self.short_term: List[str] = []
        self.long_term: List[Dict[str, List[int]]] = self._load()
        self._vocabulary: Dict[str, int] = {}
        self._rebuild_vocabulary()

    # ------------------------------------------------------------------
    def _load(self) -> List[Dict[str, List[int]]]:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.long_term, f, indent=2)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def remember(self, item: str, long_term: bool = False) -> None:
        if long_term:
            vec = self._vectorise(item)
            self.long_term.append({"text": item, "vec": vec})
            self._update_vocab(vec)
            self._save()
        else:
            self.short_term.append(item)

    def recall(self, long_term: bool = False) -> List[str]:
        if long_term:
            return [entry["text"] for entry in self.long_term]
        return list(self.short_term)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Return up to top_k most similar long-term memories."""
        if not self.long_term:
            return []
        q_vec = self._vectorise(text)
        scores = []
        for entry in self.long_term:
            score = self._cosine_similarity(q_vec, entry["vec"])
            scores.append((entry["text"], score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def clear_short_term(self) -> None:
        self.short_term.clear()

    # ------------------------------------------------------------------
    def _vectorise(self, text: str) -> List[int]:
        words = text.lower().split()
        counts = Counter(words)
        vec = [0] * len(self._vocabulary)
        for w, c in counts.items():
            idx = self._vocabulary.setdefault(w, len(self._vocabulary))
            if idx >= len(vec):
                vec.extend([0] * (idx - len(vec) + 1))
            vec[idx] = c
        return vec

    def _update_vocab(self, vec: List[int]) -> None:
        if len(vec) > len(self._vocabulary):
            self._rebuild_vocabulary()

    def _rebuild_vocabulary(self) -> None:
        self._vocabulary.clear()
        for entry in self.long_term:
            words = entry.get("text", "").lower().split()
            for w in words:
                self._vocabulary.setdefault(w, len(self._vocabulary))

    def _cosine_similarity(self, a: List[int], b: List[int]) -> float:
        length = max(len(a), len(b))
        a = a + [0] * (length - len(a))
        b = b + [0] * (length - len(b))
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
