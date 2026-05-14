from src.nlp.classification.skill_classifier import SkillClassifier
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
        self.skill_classifier = SkillClassifier()
        self.embedding_generator = EmbeddingGenerator()
        self.similarity_engine = SimilarityEngine()

    def _extract_and_classify(self, text: str) -> dict:
        skill_pairs = self.skill_extractor.extract_skills(text)["skills"]
        classified = self.skill_classifier.filter_hard_skills(skill_pairs)
        return classified

    def _process_skills(self, text: str) -> dict:
        classified = self._extract_and_classify(text)

        hard_skills = classified["hard"]
        soft_skills = classified["soft"]

        hard_embeddings = self.embedding_generator.encode(hard_skills)
        soft_embeddings = self.embedding_generator.encode(soft_skills)

        return {
            "hard_skills": hard_skills,
            "soft_skills": soft_skills,
            "hard_embeddings": hard_embeddings,
            "soft_embeddings": soft_embeddings,
        }

    def process_pdf(self, pdf_path: str) -> dict:
        raw_text = self.pdf_parser.extract_text(pdf_path)
        cleaned_text = self.text_cleaner.clean_text(raw_text)
        sections = self.section_segmenter.segment(cleaned_text)

        text_for_skills = " ".join(
            sections.get(key)
            for key in ["skills", "projects", "experience"]
            if isinstance(sections.get(key), str)
        )

        return self._process_skills(text_for_skills)

    def process_jd(self, jd_text: str) -> dict:
        cleaned_jd = self.text_cleaner.clean_text(jd_text)
        return self._process_skills(cleaned_jd)

    def analyze(self, pdf_path: str, jd_text: str) -> dict:
        resume = self.process_pdf(pdf_path)
        jd = self.process_jd(jd_text)

        return self.similarity_engine.compute(
            resume_hard_skills=resume["hard_skills"],
            jd_hard_skills=jd["hard_skills"],
            resume_hard_embeddings=resume["hard_embeddings"],
            jd_hard_embeddings=jd["hard_embeddings"],
            resume_soft_skills=resume["soft_skills"],
            jd_soft_skills=jd["soft_skills"],
            resume_soft_embeddings=resume["soft_embeddings"],
            jd_soft_embeddings=jd["soft_embeddings"],
        )
