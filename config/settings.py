import pytz
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    # TIMEZONE: str = pytz
    LOG_DIR: str = ''

    # GRPC
    GRPC_MAX_WORKERS: int
    GRPC_MAX_CONCURRENT_STREAMS: int
    GRPC_PORT: int

    # DATABASE
    DB_DSN: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    # VAULT HASHICORP # todo убрать из памяти app
    HVAC_URL: str
    HVAC_TOKEN: str
    HVAC_MASTER_KEY: str
    HMAC_KEY: str

    @property
    def default_timezone(self):
        return pytz.timezone(self.TIMEZONE)

    # Параметры из .env файла имеют приоритет выше
    class Config:
        env_file = ".env"
        extra = "ignore"  # лишнее игнорируем


settings = AppSettings() # noqa
