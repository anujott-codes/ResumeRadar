from dataclasses import dataclass, field

import requests

HF_MODEL_ID = "anujot/resumeradar-skill-classifier"


def _load_threshold() -> float:
    try:
        url = f"https://huggingface.co/{HF_MODEL_ID}/resolve/main/threshold.json"
        response = requests.get(url)
        return response.json().get("threshold", 0.5)
    except Exception:
        return 0.5


@dataclass
class SkillClassifierConfig:
    MODEL_DIR: str = HF_MODEL_ID
    MAX_LENGTH: int = 128
    BATCH_SIZE: int = 64
    THRESHOLD: float = field(default_factory=_load_threshold)
    HARD_LABEL: str = "hard"
    SOFT_LABEL: str = "soft"
