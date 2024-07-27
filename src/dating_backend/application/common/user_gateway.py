from abc import abstractmethod
from typing import Protocol

from dating_backend.application.dto import UserDTO
from dating_backend.domain.entities.user import User
from dating_backend.domain.value_objects.user_id import UserId


class UserReader(Protocol):
    @abstractmethod
    async def by_id(self, user_id: UserId) -> User | None: ...


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> UserDTO: ...
