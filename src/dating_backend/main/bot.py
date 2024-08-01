import asyncio
import logging

from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from dating_backend.bootstrap.di import setup_tg_di
from dating_backend.main.config import Config, load_config
from dating_backend.presentation.bot.setup_handlers import setup_handlers

logger = logging.getLogger(__name__)


def setup_dispatcher(config: Config) -> Dispatcher:
    dp = Dispatcher()

    setup_dishka(container=setup_tg_di(), router=dp, auto_inject=True)
    setup_handlers(dp)

    return dp


async def main():
    logging.basicConfig(level=logging.INFO)

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)

    await setup_dispatcher(config).start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
