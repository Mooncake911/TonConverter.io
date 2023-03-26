from typing import Union

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession


def create_engine(url: Union[URL, str]) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, encoding='utf-8', pool_pre_ping=True)


def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    with engine.connect() as conn:
        conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession)
