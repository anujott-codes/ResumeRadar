from typing import List, Literal

from pydantic import BaseModel, Field


class MatchedSkill(BaseModel):
    jd_skill: str = Field(..., description="Skill required by the job description.")
    matched_with: str = Field(
        ..., description="Resume skill that semantically matched the JD skill."
    )
    score: float = Field(
        ...,
        description="Similarity score between the JD skill and the matched resume skill (closer to 1.0 = stronger match).",
    )


class MissingSkill(BaseModel):
    jd_skill: str = Field(
        ..., description="JD skill that had no sufficient match in the resume."
    )
    score: float = Field(
        ...,
        description="Best similarity score found in the resume for this skill — fell below the matching threshold, so flagged as missing.",
    )


class SkillMatchCategory(BaseModel):
    matched: List[MatchedSkill] = Field(
        ..., description="Skills from the JD that were found in the resume."
    )
    missing: List[MissingSkill] = Field(
        ..., description="Skills from the JD that were not found in the resume."
    )


class PredictionResponse(BaseModel):
    coverage: float = Field(
        ..., description="Fraction of JD skills covered by the resume (0.0 to 1.0)."
    )
    hard_similarity: float = Field(
        ..., description="Average similarity score across matched hard skills."
    )
    soft_similarity: float = Field(
        ..., description="Average similarity score across matched soft skills."
    )
    final_similarity: float = Field(
        ...,
        description="Overall resume-to-JD match score combining coverage and similarity.",
    )

    hard_skills: SkillMatchCategory = Field(
        ..., description="Matched and missing hard skills."
    )
    soft_skills: SkillMatchCategory = Field(
        ..., description="Matched and missing soft skills."
    )


class HealthResponse(BaseModel):
    status: Literal["ok", "down"] = Field(
        ..., description="Health status of the API, e.g., 'ok' or 'down'."
    )
