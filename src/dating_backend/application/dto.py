from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserDTO:
    user_id: int
    full_name: str
    username: Optional[str]
