from fastapi import Request
from src.libs.exception import CustomHttpException
from fastapi.responses import JSONResponse


def error_handlers(app) -> JSONResponse:
    @app.exception_handler(CustomHttpException)
    async def http_custom_exception_handler(
        request: Request,
        exc: CustomHttpException
    ):
        content = {
            "meta": {
                "code": exc.code,
                "error": str(exc.error),
                "message": exc.message
            },
            "data": None
        }
        return JSONResponse(
            status_code=exc.code,
            content=content
        )
