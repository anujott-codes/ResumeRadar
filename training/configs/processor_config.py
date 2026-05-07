from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field


@dataclass
class ProcessorConfig:

    train_data_input_path: str = "data/staged/train.txt"
    validation_data_input_path: str = "data/staged/validation.txt"
    test_data_input_path: str = "data/staged/test.txt"

    train_data_output_path: str = "data/processed/train.csv"
    validation_data_output_path: str = "data/processed/validation.csv"
    test_data_output_path: str = "data/processed/test.csv"

    model_name: str = "facebook/bart-large-mnli"

    confidence_threshold: float = 0.75

    llm_model_name: str = "gemini-2.5-flash-lite"
    llm_batch_size: int = 64
    llm_prompt: str = """ 
    Classify each skill as HARD or SOFT.
    Rules:
    - HARD = technical, teachable, measurable (tools, programming, domain knowledge)
    - SOFT = interpersonal or behavioral

    Return ONLY valid JSON array.
    No explanation. No extra text.

    Skills: {}
    """


class LLMResponse(BaseModel):
    skill: str = Field(..., description="The skill being classified")
    label: Literal["soft", "hard"] = Field(
        ..., description="The predicted label for the skill"
    )
