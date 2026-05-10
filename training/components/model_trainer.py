import json
import os

import numpy as np
import torch
from datasets import ClassLabel, load_dataset
from sklearn.utils.class_weight import compute_class_weight
from torch import nn
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

from training.configs.training_config import TrainingConfig


class ModelTrainer:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def load_data(self):
        dataset = load_dataset(
            "csv",
            data_files={
                "train": self.config.train_path,
                "validation": self.config.val_path,
                "test": self.config.test_path,
            },
        )
        return dataset

    def train(self, dataset):
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)

        label_list = sorted(list(set(dataset["train"]["label"])))
        label2id = {label: index for index, label in enumerate(label_list)}
        id2label = {index: label for label, index in label2id.items()}

        # Encode string labels to integer IDs
        dataset = dataset.map(lambda x: self.encode_labels(x, label2id))

        # Cast the label column from string to ClassLabel so Arrow schema is correct
        class_label_feature = ClassLabel(names=label_list)
        dataset = dataset.cast_column("label", class_label_feature)

        labels = dataset["train"]["label"]
        class_weights = compute_class_weight(
            class_weight="balanced", classes=np.unique(labels), y=labels
        )
        class_weights = np.array(class_weights, dtype=np.float32)

        # Tokenize the text
        dataset = dataset.map(lambda x: self.tokenize(x, tokenizer), batched=True)

        keep_columns = ["input_ids", "attention_mask", "label"]
        dataset = dataset.remove_columns(
            [col for col in dataset["train"].column_names if col not in keep_columns]
        )
        dataset = dataset.rename_column("label", "labels")
        dataset.set_format(
            type="torch", columns=["input_ids", "attention_mask", "labels"]
        )

        data_collator = DataCollatorWithPadding(tokenizer)

        model = AutoModelForSequenceClassification.from_pretrained(
            self.config.model_name, num_labels=2, id2label=id2label, label2id=label2id
        )

        os.makedirs(self.config.model_output_dir, exist_ok=True)

        class WeightedTrainer(Trainer):
            def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
                labels = inputs.get("labels")
                outputs = model(**inputs)
                logits = outputs.get("logits")
                loss_fct = nn.CrossEntropyLoss(
                    weight=torch.tensor(class_weights).to(model.device)
                )
                loss = loss_fct(logits, labels)
                return (loss, outputs) if return_outputs else loss

        training_args = TrainingArguments(
            output_dir=self.config.model_output_dir,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            learning_rate=self.config.learning_rate,
            num_train_epochs=self.config.num_epochs,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            fp16=torch.cuda.is_available(),
            logging_steps=50,
            save_total_limit=2,
        )

        trainer = WeightedTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["validation"],
            data_collator=data_collator,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
        )

        trainer.train()
        trainer.save_model(self.config.model_output_dir)
        tokenizer.save_pretrained(self.config.model_output_dir)

        with open(f"{self.config.model_output_dir}/threshold.json", "w") as f:
            json.dump({"threshold": self.config.threshold}, f)

        return trainer

    def tokenize(self, example, tokenizer):
        return tokenizer(
            example["skill"],
            truncation=True,
            padding=False,
            max_length=self.config.max_length,
        )

    @staticmethod
    def encode_labels(example, label2id):
        label = example["label"]
        if isinstance(label, list):
            label = label[0]
        return {"label": int(label2id[str(label)])}
