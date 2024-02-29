from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASS: str

    DB_NAME: str
    COLLECTION_NAME: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
