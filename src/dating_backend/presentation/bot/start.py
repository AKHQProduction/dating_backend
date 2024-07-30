from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import FromDishka

from dating_backend.application.create_user import CreateUser, CreateUserInputDTO
from dating_backend.application.errors.user import UserIsNotExistError
from dating_backend.application.get_user import GetUser

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message, create_user: FromDishka[CreateUser], get_user: FromDishka[GetUser]
):
    try:
        await get_user(message.from_user.id)
    except UserIsNotExistError:
        await create_user(
            CreateUserInputDTO(
                user_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
            )
        )

    await message.answer("Welcome text")
