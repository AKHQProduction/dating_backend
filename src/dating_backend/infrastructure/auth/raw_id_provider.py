from dating_backend.application.common.id_provider import IdProvider
from dating_backend.domain.value_objects.user_id import UserId


class RawIdProvider(IdProvider):
    def __init__(self, user_id: UserId) -> None:
        self.user_id = user_id

    def get_current_user_id(self) -> UserId:
        return self.user_id
