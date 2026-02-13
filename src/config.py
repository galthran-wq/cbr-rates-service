from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "python-service-template"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    cors_origins: list[str] = ["*"]
    cbr_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    cbr_cache_ttl: int = 3600


settings = Settings()
