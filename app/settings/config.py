from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
