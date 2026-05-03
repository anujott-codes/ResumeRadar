import re
from typing import Dict, List

from transformers import pipeline

from src.config.skill_extractor_config import (
    DEVICE,
    HF_MODEL_NAME,
    LOWERCASE,
    ROLE_WORDS,
    SKILL_BLACKLIST,
    STRIP_PUNCT,
    THRESHOLD,
)
from src.logging.logging import get_logger

logger = get_logger(__name__)


class SkillExtractor:
    def __init__(self):
        logger.info(
            f"Initializing SkillExtractor with model={HF_MODEL_NAME} device={DEVICE}"
        )
        self._pipeline = self._load_pipeline(model=HF_MODEL_NAME, device=DEVICE)

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        if not text or not text.strip():
            logger.warning("Empty input text received for skill extraction")
            return {"skills": []}

        logger.debug(f"Running NER on text length={len(text)}")

        raw_entities = self._pipeline(text)
        logger.debug(f"Raw entities extracted: {len(raw_entities)}")

        skills = self._postprocess(raw_entities)

        logger.info(f"Final skills extracted: {len(skills)}")

        return {"skills": skills}

    def _load_pipeline(self, model: str, device: int) -> pipeline:
        logger.info("Loading HuggingFace NER pipeline...")
        return pipeline(
            "ner", model=model, aggregation_strategy="simple", device=device
        )

    def _postprocess(self, entities) -> List[str]:
        skills = []

        for ent in entities:
            label = ent.get("entity_group", "")
            word = ent.get("word", "").strip()
            score = ent.get("score", 0.0)

            if score < THRESHOLD:
                logger.debug(f"Filtered (low confidence {score:.2f}): {word}")
                continue

            if not self._is_skill_label(label):
                continue

            clean = self._normalize(word)

            if not clean:
                continue

            if clean in SKILL_BLACKLIST:
                logger.debug(f"Filtered (blacklist): {clean}")
                continue

            if clean in ROLE_WORDS:
                logger.debug(f"Filtered (role word): {clean}")
                continue

            skills.append(clean)

        logger.debug(f"Skills before deduplication: {len(skills)}")

        return self._deduplicate(skills)

    def _is_skill_label(self, label: str) -> bool:
        label = label.lower()
        return "skill" in label

    def _normalize(self, text: str) -> str:
        if LOWERCASE:
            text = text.lower()

        if STRIP_PUNCT:
            text = re.sub(r"[^\w\s\-\+\.#]", "", text)

        text = re.sub(r"-+", " ", text).strip()
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _deduplicate(self, skills: List[str]) -> List[str]:
        seen = set()
        unique = []

        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique.append(skill)

        logger.debug(f"Skills after deduplication: {len(unique)}")

        return unique
