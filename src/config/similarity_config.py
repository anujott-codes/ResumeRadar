from dataclasses import dataclass


@dataclass
class SimilarityConfig:
    THRESHOLD: float = 0.70
    WEIGHT_COVERAGE: float = 0.3
    WEIGHT_SIMILARITY: float = 0.7
    DEDUPLICATE: bool = True
