from pathlib import Path

import pymupdf

from src.exception.pdf_extraction_exception import PDFExtractionError
from src.logging.logging import get_logger

logger = get_logger(__name__)


class PDFParser:
    def extract_text(self, pdf_path: Path) -> str:
        pdf_path = Path(pdf_path)
        self._validate(pdf_path)

        logger.info(f"Extracting text from: {pdf_path.name}")

        try:
            with pymupdf.open(pdf_path) as doc:
                text = self._extract_native(doc)

                if not text.strip():
                    logger.warning(
                        f"No native text found in '{pdf_path.name}'. Falling back to OCR."
                    )
                    text = self._extract_ocr(doc)

            logger.info(
                f"Extraction complete for '{pdf_path.name}' — {len(text)} characters extracted."
            )
            return text

        except PDFExtractionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while processing '{pdf_path.name}': {e}")
            raise PDFExtractionError(
                f"Failed to extract text from '{pdf_path.name}'."
            ) from e

    def _validate(self, pdf_path: Path) -> None:
        if not pdf_path.exists():
            raise PDFExtractionError(f"File not found: {pdf_path}")
        if pdf_path.suffix.lower() != ".pdf":
            raise PDFExtractionError(f"Expected a .pdf file, got: '{pdf_path.suffix}'")

    def _extract_native(self, doc: pymupdf.Document) -> str:
        resume_text = ""
        for page in doc:
            resume_text += page.get_text() + "\n"
        return resume_text

    def _extract_ocr(self, doc: pymupdf.Document) -> str:
        try:
            pages = []
            for page in doc:
                ocr_page = page.get_textpage_ocr(language="eng", dpi=300, full=True)
                pages.append(page.get_text(textpage=ocr_page))

            text = "\n".join(pages)

            if not text.strip():
                logger.error("OCR fallback also returned empty text.")
                raise PDFExtractionError(
                    "Both native extraction and OCR returned empty text."
                )

            logger.info("OCR fallback succeeded.")
            return text

        except PDFExtractionError:
            raise
        except Exception as e:
            logger.error(f"OCR fallback failed: {e}")
            raise PDFExtractionError("OCR fallback failed.") from e
