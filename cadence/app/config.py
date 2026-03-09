from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost:5432/cadence"
    api_v1_prefix: str = "/api/v1"

    model_config = {"env_prefix": "CADENCE_"}


settings = Settings()
