from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.logger import get_logger
from app.exceptions import AppError, BadRequestError

logger = get_logger(__name__)


class ErrorResponse(BaseModel):
    """Kształt body każdej odpowiedzi błędu zwracanej przez API"""

    detail: str


class InvalidRequestDataError(BadRequestError):
    """Błąd informujący, że request nie przeszedł walidacji"""

    detail = "Invalid request data"


def error_responses(*errors: type[AppError]) -> dict[int | str, dict[str, Any]]:
    """Buduje opis odpowiedzi błędów do OpenAPI z kodu i komunikatu zapisanych w klasach wyjątków"""
    return {
        error.status_code: {
            "model": ErrorResponse,
            "description": error.detail,
            "content": {"application/json": {"example": {"detail": error.detail}}},
        }
        for error in errors
    }


async def handle_app_error(_request: Request, exc: Exception) -> JSONResponse:
    """Tłumaczy błąd domenowy na odpowiedź HTTP z kodem i komunikatem zapisanymi w wyjątku"""
    if not isinstance(exc, AppError):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    """Tłumaczy błąd walidacji requestu na 400 ze stałym komunikatem z kontraktu"""
    if not isinstance(exc, RequestValidationError):
        raise exc

    fields = ", ".join(f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors())
    logger.info("Request %s %s odrzucony przez walidację: %s", request.method, request.url.path, fields)

    return await handle_app_error(request, InvalidRequestDataError())


def register_exception_handlers(application: FastAPI) -> None:
    """Podpina handlery błędów do aplikacji"""
    application.add_exception_handler(AppError, handle_app_error)
    application.add_exception_handler(RequestValidationError, handle_validation_error)
