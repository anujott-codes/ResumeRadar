from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.backend.core.config import settings
from src.backend.schemas.response_schema import PredictionResponse
from src.backend.services.prediction_service import prediction_service

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=PredictionResponse)
async def analyze(resume: UploadFile = File(...), jd_text: str = Form(...)):
    try:
        if not jd_text or not jd_text.strip():
            raise HTTPException(
                status_code=400, detail="Job description text cannot be empty"
            )

        if not resume.filename or not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        resume.file.seek(0, 2)
        file_size = resume.file.tell()
        resume.file.seek(0)

        if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds the {settings.MAX_FILE_SIZE_MB}MB limit",
            )

        result = prediction_service.predict(resume_file=resume.file, jd_text=jd_text)

        return PredictionResponse(**result)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
