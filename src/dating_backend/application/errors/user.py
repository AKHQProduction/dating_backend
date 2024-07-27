from dating_backend.application.common.errors import ApplicationError


class UserIsNotExist(ApplicationError): ...


class UserAlreadyExists(ApplicationError): ...
