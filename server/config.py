from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    openai_assistant_id: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()
