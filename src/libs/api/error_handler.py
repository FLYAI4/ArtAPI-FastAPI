from fastapi import Request
from src.libs.api.exception import CustomHttpException
from fastapi.exceptions import RequestValidationError
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
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        content = {
            "meta": {
                "code": 422,
                "error": str(exc.errors),
                "message": "A required value is missing. Please check."
            },
            "data": None
        }
        return JSONResponse(
            status_code=422,
            content=content
        )
