import re
from typing import Optional

import spacy

from nlp.config.segmentation_config import (
    EMAIL_PATTERN,
    HEADER_MAX_WORDS,
    PHONE_PATTERN,
    SECTION_HEADER_MAP,
    SPACY_MODEL,
)
from nlp.schema.segmentation_response_schema import ResumeSegments
from src.logging.logging import get_logger

logger = get_logger(__name__)


class SectionSegmenter:

    def __init__(self) -> None:
        self._nlp = self._load_spacy()
        self._email_re = re.compile(EMAIL_PATTERN)
        self._phone_re = re.compile(PHONE_PATTERN)

        logger.info("SectionSegmenter initialized.")

    def segment(self, text: str) -> dict:
        if not text or not text.strip():
            logger.warning("Empty text passed to SectionSegmenter.")
            return ResumeSegments().to_dict()

        logger.debug("Starting segmentation process.")

        lines = text.splitlines()
        segments = ResumeSegments()

        # global fields
        segments.email = self._extract_email(text)
        segments.phone = self._extract_phone(text)
        segments.name = self._extract_name(text, lines)

        logger.debug(
            "Extracted basics | Name: %s | Email: %s | Phone: %s",
            segments.name,
            segments.email,
            segments.phone,
        )

        # section extraction
        extracted_sections = self._extract_sections(lines)

        logger.debug("Detected sections: %s", list(extracted_sections.keys()))

        for key, content in extracted_sections.items():
            if hasattr(segments, key) and content.strip():
                setattr(segments, key, content.strip())

        logger.debug("Segmentation completed.")

        return segments.to_dict()

    def _extract_email(self, text: str) -> Optional[str]:
        match = self._email_re.search(text)
        if match:
            logger.debug("Email detected.")
        return match.group(0).lower() if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        match = self._phone_re.search(text)
        if match:
            digits = re.sub(r"\D", "", match.group(0))
            if 8 <= len(digits) <= 15:
                logger.debug("Phone number detected.")
                return match.group(0).strip()
        return None

    def _extract_name(self, text: str, lines: list[str]) -> Optional[str]:
        text = text.title()
        doc = self._nlp(text[:300])

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                logger.debug("Name detected using spaCy NER.")
                name = ent.text.strip()
                name = re.split(r"[\n\d\+\|]", name)[0].strip()

                return name

        logger.debug("Name not found.")
        return None

    def _normalize_header(self, line: str) -> str:
        line = line.strip().lower()
        line = re.sub(r"[^a-z\s]", "", line)
        return line

    def _is_header(self, line: str) -> Optional[str]:
        stripped = line.strip()

        if not stripped:
            return None

        if len(stripped.split()) > HEADER_MAX_WORDS:
            return None

        normalized = self._normalize_header(stripped)

        # exact match
        if normalized in SECTION_HEADER_MAP:
            logger.debug(
                "Header detected (exact): %s -> %s",
                stripped,
                SECTION_HEADER_MAP[normalized],
            )
            return SECTION_HEADER_MAP[normalized]

        # ALL CAPS heuristic
        if stripped.isupper():
            for key in SECTION_HEADER_MAP:
                if key in normalized:
                    logger.debug(
                        "Header detected (caps): %s -> %s",
                        stripped,
                        SECTION_HEADER_MAP[key],
                    )
                    return SECTION_HEADER_MAP[key]

        # fuzzy contains
        for key in SECTION_HEADER_MAP:
            if key in normalized:
                logger.debug(
                    "Header detected (fuzzy): %s -> %s",
                    stripped,
                    SECTION_HEADER_MAP[key],
                )
                return SECTION_HEADER_MAP[key]

        return None

    def _extract_sections(self, lines: list[str]) -> dict[str, str]:
        sections: dict[str, list[str]] = {}
        current: Optional[str] = None

        for line in lines:
            canonical = self._is_header(line)

            if canonical:
                current = canonical
                sections.setdefault(current, [])
                logger.debug("Switched to section: %s", current)
                continue

            if current:
                if not line.strip():
                    continue
                sections[current].append(line)

        return {k: "\n".join(v) for k, v in sections.items()}

    @staticmethod
    def _load_spacy() -> spacy.language.Language:
        try:
            logger.info("Loading spaCy model: %s", SPACY_MODEL)
            return spacy.load(SPACY_MODEL)
        except OSError:
            logger.error(
                "spaCy model '%s' not found. Run: python -m spacy download %s",
                SPACY_MODEL,
                SPACY_MODEL,
            )
            raise
