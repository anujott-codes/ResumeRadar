from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config.embedding_generator_config import EmbeddingConfig


class EmbeddingGenerator:

    def __init__(self, config: EmbeddingConfig = EmbeddingConfig()):
        self.config = config
        self.model = self._load_model()

    def encode(self, skills: List[str]) -> np.ndarray:

        skills = self._prepare(skills)

        if not skills:
            return self._empty_embedding()

        embeddings = self.model.encode(
            skills,
            batch_size=self.config.BATCH_SIZE,
            normalize_embeddings=self.config.NORMALIZE,
            show_progress_bar=False,
        )

        return np.array(embeddings)

    def _load_model(self) -> SentenceTransformer:
        return SentenceTransformer(self.config.MODEL_NAME, device=self.config.DEVICE)

    def _prepare(self, skills: List[str]) -> List[str]:
        return [
            self._normalize_text(skill)
            for skill in skills
            if isinstance(skill, str) and skill.strip()
        ]

    def _normalize_text(self, text: str) -> str:
        return text.strip().lower()

    def _empty_embedding(self) -> np.ndarray:
        dim = self.model.get_embedding_dimension()
        return np.empty((0, dim))
