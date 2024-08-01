from dataclasses import dataclass
import logging
import os

logger = logging.getLogger(__name__)

BOT_TOKEN_ENV = "BOT_TOKEN"


class ConfigParseError(ValueError):
    pass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def get_str_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")

    return value


def load_config() -> Config:
    token = get_str_env(BOT_TOKEN_ENV)

    logger.info("Config successfuly loaded")

    return Config(tg_bot=TgBot(token=token))
