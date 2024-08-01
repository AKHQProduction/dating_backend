from dataclasses import dataclass
import logging

from dating_backend.application.common.id_provider import IdProvider
from dating_backend.application.common.interactor import Interactor
from dating_backend.application.common.user_gateway import UserReader, UserSaver
from dating_backend.domain.entities.user import User
from dating_backend.domain.value_objects.user_id import UserId


@dataclass
class AuthDTO:
    id: int
    full_name: str
    username: str | None = None


class Authenticate(Interactor[AuthDTO, UserId]):
    def __init__(
        self, id_provider: IdProvider, user_reader: UserReader, user_saver: UserSaver
    ):
        self.id_provider = id_provider
        self.user_reader = user_reader
        self.user_saver = user_saver

    async def __call__(self, data: AuthDTO) -> UserId:
        user_id = self.id_provider.get_current_user_id()

        user = await self.user_reader.by_id(user_id)

        if not user:
            logging.info("New user created %s", user_id.to_raw())
            await self.user_saver.save(
                User(user_id=user_id, full_name=data.full_name, username=data.username)
            )

        logging.info("Get user %s", user_id.to_raw())

        return user_id
