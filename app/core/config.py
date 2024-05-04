from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://cameo:password@db:5432/db"
    SYNC_DB_URL: str = "postgresql://cameo:password@db:5432/db"
    DB_DEBUG: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 260000
    SECRET_KEY: str = "9cb762ea2b00298a069fd05ee2662f9b031b71a4cdde32bb971943e3e384f06d"
    PREFIX: str = "/api"
    ALGORITHM: str = "HS256"
    OTP_LEN: int = 5
    OTP_EXPIRATION_TIMEDELTA: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
        extra = "allow"


def get_settings() -> Settings:
    return Settings()
