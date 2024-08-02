from dating_backend.domain.common.value_objects.base import ValueObject
from dating_backend.domain.errors.user import InvalidUserFullNameError


class FullName(ValueObject[str]):
    value: str

    MIN_LENGTH = 1
    MAX_LENGTH = 128

    def _validate(self) -> None:
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidUserFullNameError(
                "User full name must be greater than %d characters"
                % self.MIN_LENGTH
            )

        if len(self.value) > self.MAX_LENGTH:
            raise InvalidUserFullNameError(
                "User full name must be less than %d characters"
                % self.MAX_LENGTH
            )
