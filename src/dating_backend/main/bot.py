import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import setup_dishka

from dating_backend.bootstrap.di import setup_tg_di

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")


async def main():
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    bot = Bot(token=os.environ["BOT_TOKEN"])

    dp.include_router(router)

    setup_dishka(container=setup_tg_di(), router=dp, auto_inject=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
