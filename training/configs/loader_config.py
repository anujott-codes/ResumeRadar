from dataclasses import dataclass


@dataclass
class LoaderConfig:
    dataset_name: str = "jjzha/skillspan"
    split: str = "train"
    output_path: str = "data/raw/"
    train_data_file_path: str = "data/raw/train_data.json"
    validation_data_file_path: str = "data/raw/dev_data.json"
    test_data_file_path: str = "data/raw/test_data.json"
