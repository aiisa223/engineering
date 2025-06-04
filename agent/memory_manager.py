"""Memory management for the engineering agent."""

from __future__ import annotations

import json
import os
from typing import Dict, List, Tuple

import numpy as np

try:
    import faiss
    _HAS_FAISS = True
except Exception:  # pragma: no cover - optional dependency
    faiss = None  # type: ignore
    _HAS_FAISS = False


class MemoryManager:
    """Stores short term and persistent long term memories."""

    def __init__(self, path: str = "memory.json") -> None:
        self.path = path
        self.short_term: List[str] = []
        self.long_term: List[str] = self._load()

        # Vector dimensions for simple hashed embeddings
        self._dim = 128
        self._index = None
        self._rebuild_index()

    # ------------------------------------------------------------------
    def _load(self) -> List[str]:
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
            self.long_term.append(item)
            self._add_to_index(item)
            self._save()
        else:
            self.short_term.append(item)

    def recall(self, long_term: bool = False) -> List[str]:
        if long_term:
            return list(self.long_term)
        return list(self.short_term)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Return up to top_k most similar long-term memories."""
        if not self.long_term:
            return []
        q_vec = self._embed(text)
        if self._index is not None:
            D, I = self._index.search(q_vec.reshape(1, -1), min(top_k, len(self.long_term)))
            return [
                (self.long_term[idx], float(score))
                for idx, score in zip(I[0], D[0])
                if idx != -1
            ]
        # fallback cosine similarity
        scores = []
        for t in self.long_term:
            score = self._cosine_similarity(q_vec, self._embed(t))
            scores.append((t, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def clear_short_term(self) -> None:
        self.short_term.clear()

    # ------------------------------------------------------------------
    def _embed(self, text: str) -> np.ndarray:
        words = text.lower().split()
        vec = np.zeros(self._dim, dtype=np.float32)
        for w in words:
            idx = hash(w) % self._dim
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        if norm:
            vec /= norm
        return vec.astype("float32")

    def _add_to_index(self, text: str) -> None:
        if _HAS_FAISS:
            vec = self._embed(text).reshape(1, -1)
            if self._index is None:
                self._index = faiss.IndexFlatIP(self._dim)
            self._index.add(vec)

    def _rebuild_index(self) -> None:
        if not self.long_term or not _HAS_FAISS:
            self._index = None
            return
        self._index = faiss.IndexFlatIP(self._dim)
        vectors = np.vstack([self._embed(t) for t in self.long_term])
        self._index.add(vectors)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
