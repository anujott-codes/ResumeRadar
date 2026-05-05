import json
import os

from training.configs.extractor_config import ExtractorConfig


class SkillExtractor:
    def __init__(self, config: ExtractorConfig):
        self.config = config

    def load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def extract_skills(self, data):
        skills = []

        for row in data:
            tokens = row.get("tokens", [])
            tags = row.get("tags_skill", [])

            current_skill = []

            for token, tag in zip(tokens, tags):
                if tag == "B":
                    if current_skill:
                        skills.append(" ".join(current_skill))
                    current_skill = [token]

                elif tag == "I":
                    current_skill.append(token)

                else:  # "O"
                    if current_skill:
                        skills.append(" ".join(current_skill))
                        current_skill = []

            if current_skill:
                skills.append(" ".join(current_skill))

        return skills

    def save(self, skills, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            for skill in skills:
                f.write(skill + "\n")

    def run(self):
        # load all splits
        train_data = self.load_json(self.config.train_data_input_path)
        val_data = self.load_json(self.config.validation_data_input_path)
        test_data = self.load_json(self.config.test_data_input_path)

        # extract
        train_skills = self.extract_skills(train_data)
        val_skills = self.extract_skills(val_data)
        test_skills = self.extract_skills(test_data)

        # save
        self.save(train_skills, self.config.train_data_output_path)
        self.save(val_skills, self.config.validation_data_output_path)
        self.save(test_skills, self.config.test_data_output_path)


if __name__ == "__main__":
    config = ExtractorConfig()
    extractor = SkillExtractor(config)
    extractor.run()
