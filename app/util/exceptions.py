

class CustomBaseException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ) -> None:
        self.status_code = status_code
        super().__init__(message)


class CustomDatabaseError(CustomBaseException):
    def __str__(self):
        message = super().__str__()
        return CustomDatabaseError._extract_detail(message=message)

    @staticmethod
    def _extract_detail(message: str):
        detail = message.split("\n")[-1]
        detail = detail.split("DETAIL:")[-1]
        return detail.strip()


class ForbiddenException(CustomBaseException):
    def __init__(self, message: str, status_code: int = 403) -> None:
        super().__init__(message, status_code)


class NotFoundException(CustomBaseException):
    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message, status_code)


class BadRequestException(CustomBaseException):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message, status_code)


class ServiceUnavailableException(CustomBaseException):
    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class AuthenticationFailed(CustomBaseException):
    def __init__(
        self, message: str = "Authentication Failed", status_code: int = 401
    ) -> None:
        super().__init__(message, status_code)
