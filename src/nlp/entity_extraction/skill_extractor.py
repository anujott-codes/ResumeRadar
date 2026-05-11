import re
from typing import Dict, List, Tuple

from transformers import pipeline

from src.config.hard_skills_whitelist import HARD_SKILLS_WHITELIST
from src.config.skill_extractor_config import (
    CONTEXT_WINDOW,
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

SENTENCE_DELIMITERS = re.compile(r"[.!?\n;•|,]")


class SkillExtractor:
    def __init__(self):
        logger.info(
            f"Initializing SkillExtractor with model={HF_MODEL_NAME} device={DEVICE}"
        )
        self._pipeline = self._load_pipeline(model=HF_MODEL_NAME, device=DEVICE)

    def extract_skills(self, text: str) -> Dict[str, List[Tuple[str, str]]]:
        if not text or not text.strip():
            logger.warning("Empty input text received for skill extraction")
            return {"skills": []}

        logger.debug(f"Running NER on text length={len(text)}")

        raw_entities = self._pipeline(text)
        logger.debug(f"Raw entities extracted: {len(raw_entities)}")

        skill_pairs = self._extract_skill_pairs(text, raw_entities)

        # Keyword Fallback: Ensure whitelist skills are not missed
        whitelist_pairs = self._extract_whitelist_skills(text)
        skill_pairs.extend(whitelist_pairs)
        skill_pairs = self._deduplicate(skill_pairs)

        logger.info(f"Final skill pairs extracted (NER + Fallback): {len(skill_pairs)}")

        return {"skills": skill_pairs}

    def _load_pipeline(self, model: str, device: int) -> pipeline:
        logger.info("Loading HuggingFace NER pipeline...")
        return pipeline(
            "ner", model=model, aggregation_strategy="simple", device=device
        )

    def _extract_skill_pairs(self, text: str, entities) -> List[Tuple[str, str]]:
        pairs = []

        for ent in entities:
            label = ent.get("entity_group", "")
            word = ent.get("word", "").strip()
            score = ent.get("score", 0.0)

            if score < THRESHOLD:
                logger.debug(f"Filtered (low confidence {score:.2f}): {word}")
                continue

            if not self._is_skill_label(label):
                continue

            atomic_skill = self._normalize(word)

            if not atomic_skill:
                continue

            if atomic_skill in SKILL_BLACKLIST:
                logger.debug(f"Filtered (blacklist): {atomic_skill}")
                continue

            if atomic_skill in ROLE_WORDS:
                logger.debug(f"Filtered (role word): {atomic_skill}")
                continue

            start = ent.get("start", 0)
            end = ent.get("end", len(word))
            phrase = self._get_surrounding_phrase(text, start, end)

            pairs.append((atomic_skill, phrase))

        logger.debug(f"Pairs before deduplication: {len(pairs)}")

        return self._deduplicate(pairs)

    def _get_surrounding_phrase(self, text: str, start: int, end: int) -> str:
        window_start = max(0, start - CONTEXT_WINDOW)
        window_end = min(len(text), end + CONTEXT_WINDOW)

        left_text = text[window_start:start]
        right_text = text[end:window_end]

        left_breaks = list(SENTENCE_DELIMITERS.finditer(left_text))
        phrase_start = (
            window_start + left_breaks[-1].end() if left_breaks else window_start
        )

        right_break = SENTENCE_DELIMITERS.search(right_text)
        phrase_end = end + right_break.start() if right_break else window_end

        phrase = text[phrase_start:phrase_end].strip()
        phrase = re.sub(r"\s+", " ", phrase)

        return phrase if len(phrase) > 2 else ""

    def _extract_whitelist_skills(self, text: str) -> List[Tuple[str, str]]:
        pairs = []
        text_lower = text.lower()

        for skill in HARD_SKILLS_WHITELIST:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            for match in re.finditer(pattern, text_lower):
                start = match.start()
                end = match.end()
                phrase = self._get_surrounding_phrase(text, start, end)
                pairs.append((skill, phrase))

        return pairs

    def _is_skill_label(self, label: str) -> bool:
        label = label.lower()
        return "skill" in label and "soft" not in label

    def _normalize(self, text: str) -> str:
        if LOWERCASE:
            text = text.lower()

        if STRIP_PUNCT:
            text = re.sub(r"[^\w\s\-\+\.#]", "", text)

        text = re.sub(r"-+", " ", text).strip()
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _deduplicate(self, pairs: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        seen = set()
        unique = []

        for atomic_skill, phrase in pairs:
            key = atomic_skill.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append((atomic_skill, phrase))

        logger.debug(f"Pairs after deduplication: {len(unique)}")

        return unique
