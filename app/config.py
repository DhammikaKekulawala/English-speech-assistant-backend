from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
	OPENAI_API_KEY: str | None = None
	ENV: str = "development"
	ALLOWED_ORIGINS: str = ""
	TEMP_DIR: str = "./tmp"


class Config:
    env_file = ".env"


settings = Settings()