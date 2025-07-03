from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core import settings


class DbHelper:

    def __init__(self, url: str, echo: bool, pool_size: int, max_overflow: int):
        self._engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    async def session_getter(self):
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    async def dispose(self) -> None:
        await self._engine.dispose()

    @property
    def get_engine(self):
        return self._engine

    @property
    def get_session_factory(self):
        return self._session_factory


db_helper = DbHelper(
    url=settings.db.POSTGRES_DSN,
    echo=bool(settings.db.echo),
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
