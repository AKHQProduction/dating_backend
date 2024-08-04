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
from dating_backend.application.common.uow import UoW
from dating_backend.application.common.user_gateway import (
    UserReader,
    UserSaver,
)
from dating_backend.bootstrap.configs import load_all_configs
from dating_backend.domain.value_objects.user_id import UserId
from dating_backend.infrastructure.auth.raw_id_provider import RawIdProvider

from aiogram.types import TelegramObject, User

from dating_backend.infrastructure.gateway.user import UserGateway
from dating_backend.infrastructure.persistence.config import DBConfig
from dating_backend.infrastructure.persistence.provider import (
    get_async_session,
    get_async_sessionmaker,
    get_engine,
)
from dating_backend.infrastructure.persistence.uow import SAUnitOfWork


def gateway_provider() -> Provider:
    provider = Provider()

    provider.provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[UserReader, UserSaver],
    )

    provider.provide(
        SAUnitOfWork,
        scope=Scope.REQUEST,
        provides=UoW,
    )

    return provider


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(Authenticate, scope=Scope.REQUEST)

    return provider


def config_provider() -> Provider:
    provider = Provider()

    config = load_all_configs()

    provider.provide(lambda: config.db, scope=Scope.APP, provides=DBConfig)

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
        db_provider(),
        config_provider(),
    ]

    return providers


def setup_tg_di() -> AsyncContainer:
    providers = setup_providers()
    providers += [TgProvider()]

    container = make_async_container(*providers)

    return container
