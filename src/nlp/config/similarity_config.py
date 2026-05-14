from dataclasses import dataclass


@dataclass
class SimilarityConfig:
    THRESHOLD: float = 0.65
    WEIGHT_HARD_SIMILARITY: float = 0.7
    WEIGHT_COVERAGE: float = 0.2
    WEIGHT_SOFT_SIMILARITY: float = 0.1
    DEDUPLICATE: bool = True
