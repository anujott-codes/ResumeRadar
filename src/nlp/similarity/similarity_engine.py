from typing import Any, Dict, List

import numpy as np

from src.config.similarity_config import SimilarityConfig


class SimilarityEngine:
    def __init__(self, config: SimilarityConfig = SimilarityConfig()):
        self.config = config

    def compute(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        resume_embeddings: np.ndarray,
        jd_embeddings: np.ndarray,
    ) -> Dict[str, Any]:

        # Edge cases
        if not resume_skills or not jd_skills:
            return self._empty_result(jd_skills)

        # Step 1: similarity matrix
        sim_matrix = self._compute_similarity_matrix(resume_embeddings, jd_embeddings)

        # Step 2: best match per JD skill
        max_sim, best_idx = self._best_matches(sim_matrix)

        # Step 3: classify matched vs missing
        matched, missing = self._classify(resume_skills, jd_skills, max_sim, best_idx)

        # Step 4: optional deduplication
        if self.config.DEDUPLICATE:
            matched = self._deduplicate(matched)

        # Step 5: scoring
        coverage = self._coverage(matched, jd_skills)
        similarity_score = self._similarity_score(max_sim)
        final_score = self._final_score(coverage, similarity_score)

        return {
            "coverage": coverage,
            "similarity_score": similarity_score,
            "final_similarity": final_score,
            "matched_skills": matched,
            "missing_skills": missing,
        }

    def _compute_similarity_matrix(
        self, resume_emb: np.ndarray, jd_emb: np.ndarray
    ) -> np.ndarray:
        return resume_emb @ jd_emb.T

    def _best_matches(self, sim_matrix: np.ndarray):
        max_sim = sim_matrix.max(axis=0)
        best_idx = sim_matrix.argmax(axis=0)
        return max_sim, best_idx

    def _classify(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        max_sim: np.ndarray,
        best_idx: np.ndarray,
    ):
        matched = []
        missing = []

        for i, score in enumerate(max_sim):
            jd_skill = jd_skills[i]

            if score >= self.config.THRESHOLD:
                matched.append(
                    {
                        "jd_skill": jd_skill,
                        "matched_with": resume_skills[best_idx[i]],
                        "score": float(score),
                    }
                )
            else:
                missing.append({"jd_skill": jd_skill, "score": float(score)})

        return matched, missing

    def _deduplicate(self, matches: List[Dict]) -> List[Dict]:
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)

        used_resume = set()
        filtered = []

        for m in matches:
            if m["matched_with"] not in used_resume:
                filtered.append(m)
                used_resume.add(m["matched_with"])

        return filtered

    def _coverage(self, matched: List[Dict], jd_skills: List[str]) -> float:
        return len(matched) / len(jd_skills) if jd_skills else 0.0

    def _similarity_score(self, max_sim: np.ndarray) -> float:
        return float(np.mean(max_sim)) if len(max_sim) > 0 else 0.0

    def _final_score(self, coverage: float, similarity: float) -> float:
        return (
            self.config.WEIGHT_COVERAGE * coverage
            + self.config.WEIGHT_SIMILARITY * similarity
        )

    def _empty_result(self, jd_skills: List[str]) -> Dict[str, Any]:
        return {
            "coverage": 0.0,
            "similarity_score": 0.0,
            "final_similarity": 0.0,
            "matched_skills": [],
            "missing_skills": [
                {"jd_skill": skill, "score": 0.0} for skill in jd_skills
            ],
        }
