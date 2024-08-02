from dating_backend.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from dating_backend.application.dto import UserDTO
from dating_backend.application.errors.user import UserAlreadyExistsError
from dating_backend.domain.entities.user import User


class InMemoryUserGateway(UserSaver, UserReader):
    def __init__(self):
        self.users = {}

    async def save(self, user: User) -> UserDTO:
        user_in_db = self.users.get(user.user_id)

        if user_in_db is not None:
            raise UserAlreadyExistsError

        self.users[user.user_id] = user

        return UserDTO(
            user_id=user.user_id.to_raw(),
            full_name=user.full_name.to_raw(),
            username=user.username,
        )

    async def by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)
