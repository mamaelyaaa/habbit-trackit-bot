from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


load_dotenv()


class AppConfig(BaseModel):
    title: str = "Habbit TrackIt"
    version: str = "0.0.0"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    mode: Literal["DEV", "TEST", "PROD"]


class FilesConfig(BaseModel):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = base_dir / "src"

    # Переменные окружения
    env_file: Path = base_dir / ".env"
    env_example_file: Path = base_dir / ".env.example"

    # Логирование
    logs_dir: Path = base_dir / "logs"

    # Миграции
    alembic_dir: Path = base_dir / "migrations"


class LoggerConfig(BaseModel):
    level: Literal["DEBUG", "INFO"]
    format: str = "%(asctime)s - %(name)-16s - %(levelname)-7s - %(message)s"


class Settings(BaseSettings):
    run: RunConfig
    log: LoggerConfig
    app: AppConfig = AppConfig()
    files: FilesConfig = FilesConfig()

    model_config = SettingsConfigDict(
        env_file=(files.env_example_file, files.env_file),
        env_nested_delimiter="__",
        case_sensitive=False,
    )


settings = Settings()
