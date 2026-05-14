from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "ResumeRadar API"
    VERSION: str = "1.0.0"

    HF_NER_MODEL_NAME: str = "feliponi/hirly-ner-multi"
    SKILL_CLASSIFIER_MODEL_PATH: str = "artifacts/model"

    MAX_FILE_SIZE_MB: int = 5

    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
