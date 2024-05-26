from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_assistant_id: str

    class Config:
        env_file = ".env"

settings = Settings()
