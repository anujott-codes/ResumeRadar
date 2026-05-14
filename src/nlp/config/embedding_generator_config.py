from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
    BATCH_SIZE: int = 32
    NORMALIZE: bool = True
    DEVICE: str | None = None  # "cpu", "cuda", "mps"
