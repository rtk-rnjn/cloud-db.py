class CloudDBException(Exception):
    pass


class OnCooldown(CloudDBException):
    pass


class BadRequest(CloudDBException):
    pass


class NotFound(CloudDBException):
    pass


class HTTPException(CloudDBException):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"Something went wrong, API didn't return valid json. (Status: {status})\n\n{message}")
