import logging
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from core import settings, setup_logging
from core.exceptions import AppException

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


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    if settings.run.mode == "TEST":
        raise Exception(
            "Нельзя запустить приложение в тестовой среде. "
            "Переключите RUN__MODE на DEV или протестируйте приложение с pytest"
        )

    logger.debug(f"Приложение запущено в {settings.run.mode} среде")

    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
