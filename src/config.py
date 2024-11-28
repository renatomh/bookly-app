"""General configurations for the application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQL_HOST: str
    SQL_PORT: int
    SQL_DB: str
    SQL_USER: str
    SQL_PASS: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    @property
    def database_url(self) -> str:
        """Construct the PostgreSQL connection URL."""
        return f"postgresql+asyncpg://{self.SQL_USER}:{self.SQL_PASS}@{self.SQL_HOST}:{self.SQL_PORT}/{self.SQL_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Settings()
