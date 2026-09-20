from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.exceptions import AppError

logger = get_logger(__name__)

VALIDATION_ERROR_DETAIL = "Invalid request data"


async def handle_app_error(_request: Request, exc: Exception) -> JSONResponse:
    """Tłumaczy błąd domenowy na odpowiedź HTTP z kodem i komunikatem zapisanymi w wyjątku"""
    if not isinstance(exc, AppError):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def handle_validation_error(_request: Request, exc: Exception) -> JSONResponse:
    """Tłumaczy błąd walidacji requestu na 400 ze stałym komunikatem z kontraktu"""
    if not isinstance(exc, RequestValidationError):
        raise exc

    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"

    logger.info(message)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": VALIDATION_ERROR_DETAIL},
    )


def register_exception_handlers(application: FastAPI) -> None:
    """Podpina handlery błędów do aplikacji"""
    application.add_exception_handler(AppError, handle_app_error)
    application.add_exception_handler(RequestValidationError, handle_validation_error)
