class CustomHttpException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        self.error = None


class DBConnectionError(CustomHttpException):
    def __init__(self, code: int, message: str, err: Exception) -> None:
        super().__init__(code, message)
        self.error = err
