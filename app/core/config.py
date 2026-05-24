from functools import lru_cache

from pydantic import Field

from spend_control_shared.settings import CommonSettings


class Settings(CommonSettings):
    ollama_base_url: str = Field(default="http://ollama:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_request_timeout: int = Field(default=30, alias="OLLAMA_REQUEST_TIMEOUT")


@lru_cache
def get_settings() -> Settings:
    return Settings()

