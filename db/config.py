from os import environ

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def get_db_url():
    USER = environ["POSTGRES_USER"]
    PASSWORD = environ["POSTGRES_PASSWORD"]
    PORT = environ["POSTGRES_PORT"]
    DB = environ["POSTGRES_DB"]
    HOST = environ.get("DB_HOST", "postgres")
    return f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"


engine = create_async_engine(get_db_url(), future=True, echo=True)
async_session_maker = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)
