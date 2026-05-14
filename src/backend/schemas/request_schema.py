from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    jd_text: str = Field(..., min_length=20, description="Job description text")
