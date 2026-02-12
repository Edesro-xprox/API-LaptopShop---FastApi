from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

load_dotenv()

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    origins: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    settings.SQLALCHEMY_DATABASE_URL,
)
