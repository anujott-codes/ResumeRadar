from dataclasses import dataclass


@dataclass
class ExtractorConfig:
    train_data_input_path: str = "data/raw/train_data.json"
    train_data_output_path: str = "data/staged/train.txt"
    validation_data_input_path: str = "data/raw/dev_data.json"
    validation_data_output_path: str = "data/staged/validation.txt"
    test_data_input_path: str = "data/raw/test_data.json"
    test_data_output_path: str = "data/staged/test.txt"
