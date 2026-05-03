from src.config.base_config import SAMPLE_JD_TEXT, SAMPLE_RESUME_PDF_PATH
from src.nlp.embeddings.embedding_generator import EmbeddingGenerator
from src.nlp.entity_extraction.skill_extractor import SkillExtractor
from src.nlp.parsing.pdf_parser import PDFParser
from src.nlp.parsing.text_cleaner import TextCleaner
from src.nlp.segmentation.section_segmenter import SectionSegmenter
from src.nlp.similarity.similarity_engine import SimilarityEngine


class NLPPipeline:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.text_cleaner = TextCleaner()
        self.section_segmenter = SectionSegmenter()
        self.skill_extractor = SkillExtractor()
        self.embedding_generator = EmbeddingGenerator()
        self.similarity_engine = SimilarityEngine()

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
        resume_skills = self.skill_extractor.extract_skills(text_for_skills)["skills"]

        resume_embeddings = self.embedding_generator.encode(resume_skills)

        return resume_skills, resume_embeddings

    def process_jd(self, jd_text: str) -> dict:
        cleaned_jd = self.text_cleaner.clean_text(jd_text)
        jd_skills = self.skill_extractor.extract_skills(cleaned_jd)["skills"]
        jd_embeddings = self.embedding_generator.encode(jd_skills)

        return jd_skills, jd_embeddings

    def analyze(self, pdf_path: str, jd_text: str) -> dict:
        resume_skills, resume_embeddings = self.process_pdf(pdf_path)
        jd_skills, jd_embeddings = self.process_jd(jd_text)

        similarity_result = self.similarity_engine.compute(
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            resume_embeddings=resume_embeddings,
            jd_embeddings=jd_embeddings,
        )

        return similarity_result


if __name__ == "__main__":
    pipeline = NLPPipeline()
    result = pipeline.analyze(SAMPLE_RESUME_PDF_PATH, SAMPLE_JD_TEXT)
    print(result)
