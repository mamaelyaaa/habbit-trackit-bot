from pathlib import Path
from typing import Literal, Union

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

load_dotenv()


class AppConfig(BaseModel):
    title: str = "Habbit TrackIt"
    version: str = "0.0.0"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    mode: Literal["DEV", "TEST", "PROD"] = "DEV"


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
    alembic_ini: Path = base_dir / "alembic.ini"


class LoggerConfig(BaseModel):
    level: Literal["DEBUG", "INFO"]
    format: str = "%(asctime)s - %(name)-16s - %(levelname)-7s - %(message)s"


class DBConfig(BaseModel):
    url: Union[str, PostgresDsn]
    echo: int = 0
    pool_size: int = 10
    max_overflow: int = 10


class Settings(BaseSettings):
    log: LoggerConfig
    db: DBConfig
    run: RunConfig = RunConfig()
    app: AppConfig = AppConfig()
    files: FilesConfig = FilesConfig()

    model_config = SettingsConfigDict(
        env_file=(files.env_example_file, files.env_file),
        env_nested_delimiter="__",
        case_sensitive=False,
    )


settings = Settings()  # type: ignore[call-arg]
