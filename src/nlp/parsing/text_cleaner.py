import re

from src.logging.logging import get_logger

logger = get_logger(__name__)


class TextCleaner:

    # Bullet variants to normalize
    BULLET_PATTERN = re.compile(r"^\s*[•◦▪▸●■◆\-\*]\s+", re.MULTILINE)

    # Special characters to remove (keep alphanumeric, spaces, linebreaks, basic punctuation)
    SPECIAL_CHARS_PATTERN = re.compile(r"[^\w\s\n\.,;:()\-/&@#%+]")

    # More than 2 consecutive spaces (but not linebreaks)
    EXTRA_SPACES_PATTERN = re.compile(r"[ \t]{2,}")

    # More than 2 consecutive blank lines
    EXTRA_BLANK_LINES_PATTERN = re.compile(r"\n{3,}")

    def clean_text(self, text: str) -> str:
        if not text or not text.strip():
            logger.warning("Received empty text for cleaning.")
            return ""

        logger.info("Starting text cleaning.")

        text = self._remove_page_artifacts(text)
        text = self._lowercase(text)
        text = self._normalize_bullets(text)
        text = self._remove_special_characters(text)
        text = self._normalize_spaces(text)

        logger.info("Text cleaning complete.")
        return text.strip()

    def _remove_page_artifacts(self, text: str) -> str:
        return text.replace("\x0c", "\n")

    def _lowercase(self, text: str) -> str:
        return text.lower()

    def _normalize_bullets(self, text: str) -> str:
        return self.BULLET_PATTERN.sub("- ", text)

    def _remove_special_characters(self, text: str) -> str:
        return self.SPECIAL_CHARS_PATTERN.sub("", text)

    def _normalize_spaces(self, text: str) -> str:
        text = self.EXTRA_SPACES_PATTERN.sub(" ", text)
        text = self.EXTRA_BLANK_LINES_PATTERN.sub("\n\n", text)
        return text
