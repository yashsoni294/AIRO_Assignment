import logging
from pydantic_settings import BaseSettings
from pydantic import Field

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Application configuration loaded from .env
    """
    # OpenAI
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field("gpt-4o-mini", env="OPENAI_MODEL")

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # App Config (optional but useful)
    APP_NAME: str = "Text-to-SQL API"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton settings object
logger.info("Loading application settings")
settings = Settings()
logger.info(f"Settings loaded - App: {settings.APP_NAME}, Model: {settings.OPENAI_MODEL}, Debug: {settings.DEBUG}")
