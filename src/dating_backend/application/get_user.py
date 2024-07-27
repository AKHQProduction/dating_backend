from dating_backend.application.common.interactor import Interactor
from dating_backend.application.common.user_gateway import UserReader
from dating_backend.application.dto import UserDTO
from dating_backend.domain.value_objects.user_id import UserId


class GetUser(Interactor[int, UserDTO]):
    def __init__(self, user_reader: UserReader):
        self.user_reader = user_reader

    async def __call__(self, data: int) -> UserDTO | None:
        user_id = UserId(value=data)

        user = await self.user_reader.by_id(user_id)

        user_dto = UserDTO(
            user_id=user.user_id, 
            full_name=user.full_name,
            username=user.username
        )

        return user_dto
