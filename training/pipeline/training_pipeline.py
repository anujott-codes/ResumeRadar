from training.components.data_extractor import SkillExtractor
from training.components.data_loader import DataLoader
from training.components.data_processor import DataProcessor
from training.components.evaluator import Evaluator
from training.components.model_trainer import ModelTrainer
from training.configs.extractor_config import ExtractorConfig
from training.configs.loader_config import LoaderConfig
from training.configs.processor_config import ProcessorConfig
from training.configs.training_config import TrainingConfig


class TrainingPipeline:
    def __init__(
        self,
        training_config: TrainingConfig,
        loader_config: LoaderConfig,
        extractor_config: ExtractorConfig,
        processor_config: ProcessorConfig,
    ):
        self.training_config = training_config
        self.loader_config = loader_config
        self.extractor_config = extractor_config
        self.processor_config = processor_config

    def run(self):

        data_loader = DataLoader(self.loader_config)
        data_loader.run()

        skill_extractor = SkillExtractor(self.extractor_config)
        skill_extractor.run()

        data_processor = DataProcessor(self.processor_config)
        data_processor.run()

        model_trainer = ModelTrainer(self.training_config)
        dataset = model_trainer.load_data()
        model_trainer.train(dataset)

        evaluator = Evaluator(self.training_config)
        metrics = evaluator.evaluate()

        return metrics


if __name__ == "__main__":
    pipeline = TrainingPipeline(
        training_config=TrainingConfig(),
        loader_config=LoaderConfig(),
        extractor_config=ExtractorConfig(),
        processor_config=ProcessorConfig(),
    )
    metrics = pipeline.run()
    print(metrics)
