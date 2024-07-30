from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
)

from dating_backend.application.common.user_gateway import UserReader, UserSaver
from dating_backend.application.create_user import CreateUser
from dating_backend.application.get_user import GetUser
from dating_backend.infrastructure.gateway.in_memory import InMemoryUserGateway


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


def setup_providers() -> list[Provider]:
    providers = [
        gateway_provider(),
        interactor_provider(),
    ]

    return providers


def setup_tg_di() -> AsyncContainer:
    providers = setup_providers()

    container = make_async_container(*providers)

    return container
