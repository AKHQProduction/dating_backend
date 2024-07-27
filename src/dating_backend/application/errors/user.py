from dating_backend.application.common.errors import ApplicationError


class UserIsNotExistError(ApplicationError): ...


class UserAlreadyExistsError(ApplicationError): ...
