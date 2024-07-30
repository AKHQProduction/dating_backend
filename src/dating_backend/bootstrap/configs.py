from dataclasses import dataclass
import logging
import os


@dataclass
class BotConfig:
    token: str


@dataclass
class AllConfigs:
    bot: BotConfig


def load_all_configs() -> AllConfigs:
    bot_config = BotConfig(token=os.environ["BOT_TOKEN"])

    logging.info("Config loaded.")

    return AllConfigs(bot=bot_config)
