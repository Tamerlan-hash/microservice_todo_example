import logging

from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.settings.config import SQLALCHEMY_DATABASE_URL


logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=0,
    echo=True,
)

async_session = sessionmaker(
    bind=async_engine, autoflush=False, future=True, class_=AsyncSession
)
Base = declarative_base()


async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield async_session
    except SQLAlchemyError as e:
        logger.exception(e)