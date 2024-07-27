import logging

from dataclasses import dataclass
from typing import Optional

from dating_backend.application.common.interactor import Interactor
from dating_backend.application.common.user_gateway import UserSaver
from dating_backend.application.dto import UserDTO
from dating_backend.domain.entities.user import User
from dating_backend.domain.value_objects.user_id import UserId


@dataclass(frozen=True)
class CreateUserInputDTO:
    user_id: int
    full_name: str
    username: Optional[str]


class CreateUser(Interactor[CreateUserInputDTO, UserDTO]):
    def __init__(self, user_gateway: UserSaver):
        self.user_gateway = user_gateway

    async def __call__(self, data: CreateUserInputDTO) -> UserDTO:
        user_id = UserId(value=data.user_id)

        user = User(
            user_id=user_id,
            full_name=data.full_name,
            username=data.username,
        )

        user_dto = await self.user_gateway.save(user=user)

        logging.info("User created with id: %s", str(user_id.to_raw()))

        return user_dto
