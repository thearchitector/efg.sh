from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

SessionMaker = async_sessionmaker[AsyncSession]


def sessionmaker_factory() -> SessionMaker:
    return async_sessionmaker(
        create_async_engine("triopg://postgres:password@db/postgres")
    )
