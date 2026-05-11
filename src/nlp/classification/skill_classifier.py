from typing import Dict, List, Tuple

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.config.hard_skills_whitelist import HARD_SKILLS_WHITELIST
from src.config.skill_classifier_config import SkillClassifierConfig
from src.logging.logging import get_logger

logger = get_logger(__name__)


class SkillClassifier:
    def __init__(self, config: SkillClassifierConfig = SkillClassifierConfig()):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.MODEL_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.MODEL_DIR
        )
        self.model.eval()
        self.id2label = self.model.config.id2label
        logger.info(f"SkillClassifier loaded from {config.MODEL_DIR}")

    def classify(
        self, skill_pairs: List[Tuple[str, str]]
    ) -> List[Tuple[str, str, float]]:
        if not skill_pairs:
            return []

        phrases = [phrase for _, phrase in skill_pairs]
        atomic_skills = [skill for skill, _ in skill_pairs]

        results = []
        for i in range(0, len(phrases), self.config.BATCH_SIZE):
            batch_phrases = phrases[i : i + self.config.BATCH_SIZE]
            batch_skills = atomic_skills[i : i + self.config.BATCH_SIZE]
            results.extend(self._classify_batch(batch_skills, batch_phrases))
        return results

    def filter_hard_skills(
        self, skill_pairs: List[Tuple[str, str]]
    ) -> Dict[str, List[str]]:
        classified = self.classify(skill_pairs)
        hard = [s for s, label, _ in classified if label == self.config.HARD_LABEL]
        soft = [s for s, label, _ in classified if label == self.config.SOFT_LABEL]
        logger.info(
            f"Classified {len(hard)} hard, {len(soft)} soft from {len(skill_pairs)} skills"
        )
        return {"hard": hard, "soft": soft}

    def _classify_batch(
        self, atomic_skills: List[str], phrases: List[str]
    ) -> List[Tuple[str, str, float]]:
        inputs = self.tokenizer(
            phrases,
            truncation=True,
            padding=True,
            max_length=self.config.MAX_LENGTH,
            return_tensors="pt",
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.softmax(logits, dim=-1).numpy()
        soft_probs = probs[:, 1]

        results = []
        for idx, skill in enumerate(atomic_skills):
            if skill.lower() in HARD_SKILLS_WHITELIST:
                label = self.config.HARD_LABEL
                confidence = 1.0
            else:
                is_soft = soft_probs[idx] >= self.config.THRESHOLD
                label = self.config.SOFT_LABEL if is_soft else self.config.HARD_LABEL
                confidence = (
                    float(soft_probs[idx]) if is_soft else float(1 - soft_probs[idx])
                )
            results.append((skill, label, confidence))

        return results
