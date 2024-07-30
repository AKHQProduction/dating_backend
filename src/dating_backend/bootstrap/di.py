from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)

from dating_backend.application.common.user_gateway import UserReader, UserSaver
from dating_backend.application.create_user import CreateUser
from dating_backend.application.get_user import GetUser
from dating_backend.infrastructure.gateway.in_memory import InMemoryUserGateway
from aiogram.types import TelegramObject, User


def gateway_provider() -> Provider:
    provider = Provider()

    provider.provide(
        InMemoryUserGateway, scope=Scope.REQUEST, provides=AnyOf[UserReader, UserSaver]
    )

    return provider


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(CreateUser, scope=Scope.REQUEST)
    provider.provide(GetUser, scope=Scope.REQUEST)

    return provider


class TGProvider(Provider):
    telegram_object = from_context(provides=TelegramObject, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(self, obj: TelegramObject) -> User:
        return obj.from_user


def setup_providers() -> list[Provider]:
    providers = [
        gateway_provider(),
        interactor_provider(),
    ]

    return providers


def setup_tg_di() -> AsyncContainer:
    providers = setup_providers()
    providers += [TGProvider()]

    container = make_async_container(*providers)

    return container
