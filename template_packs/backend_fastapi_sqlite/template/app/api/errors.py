from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError


async def handle_app_error(_request: Request, exc: Exception) -> JSONResponse:
    """Tłumaczy błąd domenowy na odpowiedź HTTP z kodem i komunikatem zapisanymi w wyjątku"""
    if not isinstance(exc, AppError):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def register_exception_handlers(application: FastAPI) -> None:
    """Podpina handlery błędów do aplikacji"""
    application.add_exception_handler(AppError, handle_app_error)
