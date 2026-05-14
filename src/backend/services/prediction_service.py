import os
import tempfile
from typing import Any, Dict

from src.nlp.pipeline.nlp_pipeline import NLPPipeline


class PredictionService:

    def __init__(self):
        self.pipeline = NLPPipeline()

    def _save_temp_pdf(self, file) -> str:
        """Save uploaded PDF to a temporary file and return path"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            return tmp.name

    def _round_scores(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Round float values for cleaner API response"""

        def round_float(x):
            return round(x, 3) if isinstance(x, float) else x

        if isinstance(data, dict):
            return {k: self._round_scores(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._round_scores(i) for i in data]
        else:
            return round_float(data)

    def _format_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Map pipeline output → API response schema"""

        return {
            "coverage": result.get("coverage"),
            "hard_similarity": result.get("hard_similarity"),
            "soft_similarity": result.get("soft_similarity"),
            "final_similarity": result.get("final_similarity"),
            "hard_skills": {
                "matched": result.get("matched_hard_skills", []),
                "missing": result.get("missing_hard_skills", []),
            },
            "soft_skills": {
                "matched": result.get("matched_soft_skills", []),
                "missing": result.get("missing_soft_skills", []),
            },
        }

    def predict(self, resume_file, jd_text: str) -> Dict[str, Any]:
        temp_path = None

        try:
            temp_path = self._save_temp_pdf(resume_file)

            result = self.pipeline.analyze(temp_path, jd_text)

            result = self._round_scores(result)

            formatted = self._format_response(result)

            return formatted

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


prediction_service = PredictionService()
