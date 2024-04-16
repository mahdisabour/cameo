"""
    Backend Main module
"""

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.db.session import get_session
from app.util.exceptions import (
    AuthenticationFailed,
    BadRequestException,
    CustomDatabaseError,
    ForbiddenException,
    NotFoundException,
)


def get_application() -> FastAPI:
    application = FastAPI(
        version="1.0.0", title="cameo", dependencies=[Depends(get_session)]
    )
    return application


app: FastAPI = get_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomDatabaseError)
async def custom_database_error_handler(request: Request, exc: CustomDatabaseError):
    return JSONResponse(content={"detail": str(exc)}, status_code=exc.status_code)


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(content={"detail": str(exc)}, status_code=exc.status_code)


@app.exception_handler(NotFoundException)
async def forbidden_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(content={"detail": str(exc)}, status_code=exc.status_code)


@app.exception_handler(BadRequestException)
async def forbidden_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(content={"detail": str(exc)}, status_code=exc.status_code)


@app.exception_handler(AuthenticationFailed)
async def forbidden_exception_handler(request: Request, exc: AuthenticationFailed):
    return JSONResponse(content={"detail": str(exc)}, status_code=exc.status_code)
