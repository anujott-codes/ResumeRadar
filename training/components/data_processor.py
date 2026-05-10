import csv
import json
import os

from dotenv import load_dotenv
from google import genai
from transformers import pipeline

from training.configs.processor_config import LLMResponse, ProcessorConfig

load_dotenv()


class DataProcessor:
    def __init__(self, config: ProcessorConfig):
        self.config = config

        self.classifier = pipeline(
            "zero-shot-classification", model=self.config.model_name
        )

        self.llm_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def load_file(self, path):
        with open(path, "r") as f:
            skills = [line.strip() for line in f if line.strip()]
        return list(set(skills))

    def classify_zero_shot(self, skills):
        confident_results = []
        uncertain_skills = []

        for skill in skills:
            output = self.classifier(
                f"{skill} is a", candidate_labels=["soft skill", "hard skill"]
            )

            score = output["scores"][0]
            label = output["labels"][0]

            if score >= self.config.confidence_threshold:
                final_label = "soft" if label == "soft skill" else "hard"
                confident_results.append((skill, final_label))
            else:
                uncertain_skills.append(skill)

        return confident_results, uncertain_skills

    def classify_llm_batch(self, skills):
        results = []
        if not skills:
            return results

        batch_size = self.config.llm_batch_size
        prompt_template = self.config.llm_prompt

        for i in range(0, len(skills), batch_size):
            batch = skills[i : i + batch_size]

            batch_str = "\n".join(batch)
            prompt = prompt_template.format(batch_str)

            response = self.llm_client.models.generate_content(
                model=self.config.llm_model_name,
                contents=prompt,
                config={
                    "temperature": 0,
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "array",
                        "items": LLMResponse.model_json_schema(),
                    },
                },
            )

            text = response.text.strip()

            try:
                parsed = json.loads(text)
            except Exception:
                continue

            for item in parsed:
                results.append((item["skill"], item["label"]))

        return results

    def classify(self, skills):
        # zero-shot on all skills
        confident_results, uncertain_skills = self.classify_zero_shot(skills)

        # LLM only for low-confidence cases
        llm_results = self.classify_llm_batch(uncertain_skills)

        return confident_results + llm_results

    def save(self, data, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["skill", "label"])
            writer.writerows(data)

    def process_split(self, input_path, output_path):
        skills = self.load_file(input_path)
        labeled_data = self.classify(skills)
        self.save(labeled_data, output_path)

    def run(self):
        self.process_split(
            self.config.train_data_input_path, self.config.train_data_output_path
        )

        self.process_split(
            self.config.validation_data_input_path,
            self.config.validation_data_output_path,
        )

        self.process_split(
            self.config.test_data_input_path, self.config.test_data_output_path
        )
