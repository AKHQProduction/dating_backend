from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from dishka import FromDishka

from dating_backend.application.authenticate import AuthDTO, Authenticate


router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message, action: FromDishka[Authenticate], user: FromDishka[User]
):
    await action(
        AuthDTO(id=user.id, full_name=user.full_name, username=user.username)
    )

    await message.answer("Welcome text")
