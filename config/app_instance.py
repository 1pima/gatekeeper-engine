import pytz
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    TIMEZONE: str = pytz
    LOG_DIR: str = ''

    @property
    def default_timezone(self):
        return pytz.timezone(self.TIMEZONE)

    # Параметры из .env файла имеют приоритет выше
    class Config:
        env_file = ".env"
        extra = "ignore"  # лишнее игнорируем


app_config = AppConfig()  # noqa
