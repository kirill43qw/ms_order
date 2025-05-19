from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "ms_order"
    API_KEY: str = "api_key_ms_order"
    APP_ENV: str

    DB_URL: str
    DB_SCHEMA: str
    RABBITMQ_URL: str


settings = Settings()
