import json
import os

import numpy as np
from datasets import Value, load_dataset
from sklearn.metrics import classification_report
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
)

from training.configs.training_config import TrainingConfig


class Evaluator:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def load_model(self):
        """Load trained model and tokenizer from artifacts/model."""
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.config.model_output_dir
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_output_dir)

        self.trainer = Trainer(
            model=self.model, data_collator=DataCollatorWithPadding(self.tokenizer)
        )

    def tokenize(self, example):
        return self.tokenizer(
            example["skill"], truncation=True, max_length=self.config.max_length
        )

    def evaluate(self):
        """Load trained model, prepare test data, and evaluate."""
        # Step 1: Load the trained model from disk
        self.load_model()

        # Step 2: Load test dataset from processed CSV
        dataset = load_dataset("csv", data_files={"test": self.config.test_path})

        # Step 3: Encode string labels to integer IDs using the model's label mapping
        label2id = self.model.config.label2id
        dataset = dataset.map(lambda x: {"label": int(label2id[str(x["label"])])})
        # Cast label column to int64 so the Arrow schema matches the actual values
        dataset = dataset.cast_column("label", Value("int64"))

        # Step 4: Tokenize test data
        dataset = dataset.map(self.tokenize, batched=True)

        # Step 5: Keep only model-relevant columns
        keep_columns = ["input_ids", "attention_mask", "label"]
        dataset = dataset.remove_columns(
            [col for col in dataset["test"].column_names if col not in keep_columns]
        )
        dataset = dataset.rename_column("label", "labels")

        # Step 6: Run predictions
        preds_output = self.trainer.predict(dataset["test"])

        logits = preds_output.predictions
        labels = preds_output.label_ids

        probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
        soft_probs = probs[:, 1]

        threshold = self.config.threshold
        preds = (soft_probs >= threshold).astype(int)

        report = classification_report(labels, preds, output_dict=True)

        # Step 5: Save metrics
        os.makedirs(os.path.dirname(self.config.metrics_output_path), exist_ok=True)

        with open(self.config.metrics_output_path, "w") as f:
            json.dump(report, f, indent=4)

        return report
