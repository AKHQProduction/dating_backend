import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from dishka.integrations.aiogram import setup_dishka

from dating_backend.bootstrap.di import setup_tg_di
from dating_backend.presentation.bot.setup_handlers import setup_handlers

router = Router()


async def main():
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    bot = Bot(token=os.environ["BOT_TOKEN"])

    setup_dishka(container=setup_tg_di(), router=dp, auto_inject=True)
    setup_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
