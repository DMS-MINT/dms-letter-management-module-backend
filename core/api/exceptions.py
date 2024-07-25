from rest_framework import status as http_status


class ApplicationError(Exception):
    def __init__(
        self,
        error_code: str,
        message=None,
        extra=None,
    ):
        super().__init__(message)

        self.error_code = error_code
        self.message = message
        self.extra = extra or {}


class APIError(Exception):
    def __init__(
        self,
        error_code: str,
        status_code=http_status.HTTP_400_BAD_REQUEST,
        message="An error occurred",
        extra=None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code
        self.message = message
        self.extra = extra or {}

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message, "extra": self.extra}
