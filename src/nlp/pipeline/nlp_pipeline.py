from src.config.base_config import SAMPLE_RESUME_PDF_PATH
from src.nlp.entity_extraction.skill_extractor import SkillExtractor
from src.nlp.parsing.pdf_parser import PDFParser
from src.nlp.parsing.text_cleaner import TextCleaner
from src.nlp.segmentation.section_segmenter import SectionSegmenter


class NLPPipeline:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.text_cleaner = TextCleaner()
        self.section_segmenter = SectionSegmenter()
        self.skill_extractor = SkillExtractor()

    def process_pdf(self, pdf_path: str) -> dict:
        # Step 1: Extract text from PDF
        raw_text = self.pdf_parser.extract_text(pdf_path)

        # Step 2: Clean the extracted text
        cleaned_text = self.text_cleaner.clean_text(raw_text)

        # Step 3: Segment the cleaned text into sections
        sections = self.section_segmenter.segment(cleaned_text)

        # Step 4: Extract skills from the entire cleaned text
        text_for_skills = " ".join(
            sections.get(key)
            for key in ["skills", "projects", "experience"]
            if isinstance(sections.get(key), str)
        )
        skills = self.skill_extractor.extract_skills(text_for_skills)

        return skills


if __name__ == "__main__":
    pipeline = NLPPipeline()
    skills = pipeline.process_pdf(SAMPLE_RESUME_PDF_PATH)
    print(skills)
