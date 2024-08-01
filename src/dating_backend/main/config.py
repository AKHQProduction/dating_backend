from dataclasses import dataclass
import logging
from environs import Env


@dataclass
class TgBot:
    token: str

    @staticmethod
    def from_env(env: Env) -> "TgBot":
        token = env.str("BOT_TOKEN")

        return TgBot(token=token)


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    env = Env()
    env.read_env(".env")

    config = Config(tg_bot=TgBot.from_env(env))

    logging.info("Config successfuly loaded")

    return config
