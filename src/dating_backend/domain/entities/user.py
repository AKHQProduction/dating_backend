from dataclasses import dataclass
from typing import Optional, Union

from dating_backend.domain.value_objects.user_id import UserId


@dataclass
class User:
    user_id: UserId
    full_name: str
    username: Optional[str]
    is_active: Optional[bool] = True

    def __hash__(self) -> int:
        return hash(self.user_id)

    def __eq__(self, other: Union[object, "User"]) -> bool:
        if not isinstance(other, User):
            return False

        return self.user_id == other.user_id

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__} object(id={self.user_id}, is_active"
            f"={bool(self)})"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__} <{self.user_id}>"
