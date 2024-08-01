from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)

from dating_backend.application.authenticate import Authenticate
from dating_backend.application.common.id_provider import IdProvider
from dating_backend.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from dating_backend.domain.value_objects.user_id import UserId
from dating_backend.infrastructure.auth.raw_id_provider import RawIdProvider
from dating_backend.infrastructure.gateway.in_memory import InMemoryUserGateway

from aiogram.types import TelegramObject, User


def gateway_provider() -> Provider:
    provider = Provider()

    provider.provide(
        InMemoryUserGateway,
        scope=Scope.APP,
        provides=AnyOf[UserReader, UserSaver],
    )

    return provider


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(Authenticate, scope=Scope.REQUEST)

    return provider


class TgProvider(Provider):
    tg_object = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_user(self, obj: TelegramObject) -> User:
        return obj.from_user

    @provide(scope=Scope.REQUEST)
    async def get_id_provider(self, obj: TelegramObject) -> IdProvider:
        return RawIdProvider(UserId(obj.from_user.id))


def setup_providers() -> list[Provider]:
    providers = [
        gateway_provider(),
        interactor_provider(),
    ]

    return providers


def setup_tg_di() -> AsyncContainer:
    providers = setup_providers()
    providers += [TgProvider()]

    container = make_async_container(*providers)

    return container
