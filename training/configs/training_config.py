from dataclasses import dataclass


@dataclass
class TrainingConfig:
    model_name: str = "distilbert-base-uncased"
    max_length: int = 16
    batch_size: int = 64
    learning_rate: float = 3e-5
    num_epochs: int = 5
    threshold: float = 0.5

    train_path: str = "data/processed/train.csv"
    val_path: str = "data/processed/validation.csv"
    test_path: str = "data/processed/test.csv"

    model_output_dir: str = "artifacts/model"
    metrics_output_path: str = "artifacts/metrics/metrics.json"
