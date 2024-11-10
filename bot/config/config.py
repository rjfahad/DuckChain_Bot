from pydantic_settings import BaseSettings, SettingsConfigDict
from bot.utils import logger
import sys

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int = 12345
    API_HASH: str = 'abcd'
   
    REF_ID: str = 'KvNYn05S'
    SUPPORT_AUTHOR: bool = True
    OPEN_BOX: bool = True
    AUTO_TASK: bool = True
    AUTO_QUACK: bool = True
    TOTAL_QUACK: list[int] = [1, 5]
    QUACK_DELAY: list[float] = [1, 2]
    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: list[int] = [0, 15]
    FAKE_USERAGENT: bool = True
    SLEEP_TIME: list[int] = [400, 1000]
    
    USE_PROXY_FROM_FILE: bool = False


settings = Settings()

if settings.API_ID == 12345 and settings.API_HASH == 'abcd':
    sys.exit(logger.info("<r>Please edit API_ID and API_HASH from .env file to continue.</r>"))

if settings.API_ID == 12345:
    sys.exit(logger.info("Please edit API_ID from .env file to continue."))

if settings.API_HASH == 'abcd':
    sys.exit(logger.info("Please edit API_HASH from .env file to continue."))