import json
import os

from datasets import load_dataset

from training.configs.loader_config import LoaderConfig


class DataLoader:
    def __init__(self, config: LoaderConfig):
        self.config = config

    def load(self):
        dataset = load_dataset(self.config.dataset_name)
        return dataset

    def save_training_data(self, dataset):
        os.makedirs(self.config.output_path, exist_ok=True)

        with open(self.config.train_data_file_path, "w") as f:
            json.dump(dataset["train"].to_list(), f, indent=2)

    def save_validation_data(self, dataset):
        os.makedirs(self.config.output_path, exist_ok=True)

        with open(self.config.validation_data_file_path, "w") as f:
            json.dump(dataset["validation"].to_list(), f, indent=2)

    def save_test_data(self, dataset):
        os.makedirs(self.config.output_path, exist_ok=True)

        with open(self.config.test_data_file_path, "w") as f:
            json.dump(dataset["test"].to_list(), f, indent=2)

    def run(self):
        dataset = self.load()
        self.save_training_data(dataset)
        self.save_validation_data(dataset)
        self.save_test_data(dataset)
