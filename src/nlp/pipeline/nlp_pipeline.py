from src.nlp.parsing.pdf_parser import PDFParser
from src.nlp.parsing.text_cleaner import TextCleaner
from src.nlp.segmentation.section_segmenter import SectionSegmenter


class NLPPipeline:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.text_cleaner = TextCleaner()
        self.section_segmenter = SectionSegmenter()

    def process_pdf(self, pdf_path: str) -> dict:
        # Step 1: Extract text from PDF
        raw_text = self.pdf_parser.extract_text(pdf_path)

        # Step 2: Clean the extracted text
        cleaned_text = self.text_cleaner.clean_text(raw_text)

        # Step 3: Segment the cleaned text into sections
        sections = self.section_segmenter.segment(cleaned_text)

        return sections


if __name__ == "__main__":
    pipeline = NLPPipeline()
    pdf_path = "10554236.pdf"
    sections = pipeline.process_pdf(pdf_path)
    print(sections)
