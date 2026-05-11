import json
from dataclasses import dataclass, field
from pathlib import Path

MODEL_DIR = Path("artifacts/model")
THRESHOLD_FILE = MODEL_DIR / "threshold.json"


def _load_threshold() -> float:
    if THRESHOLD_FILE.exists():
        with open(THRESHOLD_FILE) as f:
            return json.load(f).get("threshold", 0.5)
    return 0.5


@dataclass
class SkillClassifierConfig:
    MODEL_DIR: str = str(MODEL_DIR)
    MAX_LENGTH: int = 128
    BATCH_SIZE: int = 64
    THRESHOLD: float = field(default_factory=_load_threshold)
    HARD_LABEL: str = "hard"
    SOFT_LABEL: str = "soft"
