from typing import Any, Dict, List

import numpy as np

from nlp.config.similarity_config import SimilarityConfig


class SimilarityEngine:
    def __init__(self, config: SimilarityConfig = SimilarityConfig()):
        self.config = config

    def compute(
        self,
        resume_hard_skills: List[str],
        jd_hard_skills: List[str],
        resume_hard_embeddings: np.ndarray,
        jd_hard_embeddings: np.ndarray,
        resume_soft_skills: List[str],
        jd_soft_skills: List[str],
        resume_soft_embeddings: np.ndarray,
        jd_soft_embeddings: np.ndarray,
    ) -> Dict[str, Any]:

        hard_result = self._compute_skill_group(
            resume_hard_skills,
            jd_hard_skills,
            resume_hard_embeddings,
            jd_hard_embeddings,
        )

        soft_result = self._compute_skill_group(
            resume_soft_skills,
            jd_soft_skills,
            resume_soft_embeddings,
            jd_soft_embeddings,
        )

        coverage = hard_result["coverage"]
        hard_similarity = hard_result["similarity"]
        soft_similarity = soft_result["similarity"]

        final_score = self._final_score(hard_similarity, coverage, soft_similarity)

        return {
            "coverage": coverage,
            "hard_similarity": hard_similarity,
            "soft_similarity": soft_similarity,
            "final_similarity": final_score,
            "matched_hard_skills": hard_result["matched"],
            "missing_hard_skills": hard_result["missing"],
            "matched_soft_skills": soft_result["matched"],
            "missing_soft_skills": soft_result["missing"],
        }

    def _compute_skill_group(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        resume_embeddings: np.ndarray,
        jd_embeddings: np.ndarray,
    ) -> Dict[str, Any]:

        if not resume_skills or not jd_skills:
            return {
                "coverage": 0.0,
                "similarity": 0.0,
                "matched": [],
                "missing": [{"jd_skill": s, "score": 0.0} for s in (jd_skills or [])],
            }

        sim_matrix = self._compute_similarity_matrix(resume_embeddings, jd_embeddings)
        max_sim, best_idx = self._best_matches(sim_matrix)
        matched, missing = self._classify(resume_skills, jd_skills, max_sim, best_idx)

        if self.config.DEDUPLICATE:
            matched, dropped = self._deduplicate(matched)
            missing.extend(dropped)

        coverage = self._coverage(matched, jd_skills)
        similarity = self._similarity_score(max_sim)

        return {
            "coverage": coverage,
            "similarity": similarity,
            "matched": matched,
            "missing": missing,
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

    def _deduplicate(self, matches: List[Dict]):
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)

        used_resume = set()
        kept = []
        dropped = []

        for m in matches:
            if m["matched_with"] not in used_resume:
                kept.append(m)
                used_resume.add(m["matched_with"])
            else:
                dropped.append({"jd_skill": m["jd_skill"], "score": m["score"]})

        return kept, dropped

    def _coverage(self, matched: List[Dict], jd_skills: List[str]) -> float:
        return len(matched) / len(jd_skills) if jd_skills else 0.0

    def _similarity_score(self, max_sim: np.ndarray) -> float:
        return float(np.mean(max_sim)) if len(max_sim) > 0 else 0.0

    def _final_score(
        self, hard_similarity: float, coverage: float, soft_similarity: float
    ) -> float:
        return (
            self.config.WEIGHT_HARD_SIMILARITY * hard_similarity
            + self.config.WEIGHT_COVERAGE * coverage
            + self.config.WEIGHT_SOFT_SIMILARITY * soft_similarity
        )
