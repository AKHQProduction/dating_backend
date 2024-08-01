import asyncio
import logging

from aiogram import Bot, Dispatcher
from dishka.integrations.aiogram import setup_dishka

from dating_backend.bootstrap.di import setup_tg_di
from dating_backend.main.config import Config, load_config
from dating_backend.presentation.bot.setup_handlers import setup_handlers


async def main():
    logging.basicConfig(level=logging.INFO)

    config: Config = load_config()

    dp = Dispatcher()
    bot = Bot(token=config.tg_bot.token)

    setup_dishka(container=setup_tg_di(), router=dp, auto_inject=True)
    setup_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
