from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.config import settings

# Create a database engine to connect with database
engine = create_async_engine(
    # database type/dialect and file name
    url=settings.POSTGRES_URL,
    # Log sql queries
    echo=True,
)

from .models import Shipment

# 匯入模型 = 讓類別定義生效
# create_db_tables() 才能看到所有已定義的資料表結構
# 否則即使呼叫 create_all()，也可能只建立空的或不完整的資料庫結構


async def create_db_tables():
    async with engine.begin() as connection:
        from app.api.schemas.shipments import Shipment
        await connection.run_sync(SQLModel.metadata.create_all)


# Session to interact with database
async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


# Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]
