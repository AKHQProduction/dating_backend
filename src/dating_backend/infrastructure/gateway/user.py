from sqlalchemy import select
from dating_backend.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from dating_backend.application.dto import UserDTO
from dating_backend.application.errors.user import UserAlreadyExistsError
from dating_backend.domain.entities.user import User
from dating_backend.domain.value_objects.full_name import FullName
from dating_backend.domain.value_objects.user_id import UserId
from dating_backend.infrastructure.persistence.models.user import UserORM


class UserGateway(UserSaver, UserReader):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def save(self, user: User) -> UserDTO:
        db_user = UserORM(
            user_id=user.user_id.to_raw(),
            full_name=user.full_name.to_raw(),
            username=user.username,
        )

        try:
            await self.session.merge(db_user)
        except IntegrityError as err:
            raise UserAlreadyExistsError(
                f"User with id {user.user_id} already exists"
            ) from err

        return UserDTO(
            user_id=db_user.user_id,
            full_name=db_user.full_name,
            username=db_user.username,
        )

    async def by_id(self, user_id: UserId) -> User | None:
        query = select(UserORM).where(UserORM.user_id == user_id.to_raw())

        result = await self.session.execute(query)

        user: UserORM | None = result.scalar()

        if not user:
            return None
        return User(
            user_id=UserId(user.user_id),
            full_name=FullName(user.full_name),
            username=user.username,
            is_active=user.is_active,
        )
