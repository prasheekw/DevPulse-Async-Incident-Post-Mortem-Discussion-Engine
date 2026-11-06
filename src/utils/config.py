from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_UNPOOLED: str | None = None
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings() # pyright: ignore[reportCallIssue]