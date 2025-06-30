import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import text

from src.core import settings, setup_logging, SessionDep
from src.core.exceptions import AppException
from src.schemas import BaseResponseModel

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app.title,
    version=settings.app.version,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)


@app.get("/", response_model=BaseResponseModel)
def get_root():
    return BaseResponseModel(detail="Api is working!")


@app.get("/health-check", response_model=BaseResponseModel)
async def check_db_conn(session: SessionDep):
    query = await session.scalar(text("SELECT VERSION()"))
    return BaseResponseModel(detail=str(query))


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    if settings.run.mode == "TEST":
        raise Exception(
            "Нельзя запустить приложение в тестовой среде. "
            "Переключите RUN__MODE на DEV или протестируйте приложение с pytest"
        )

    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
