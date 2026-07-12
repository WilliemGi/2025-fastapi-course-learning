from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

engine = create_engine(
    url="sqlite:///sqlite_new.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

from .models import Shipment

# 匯入模型 = 讓類別定義生效
# create_db_tables() 才能看到所有已定義的資料表結構
# 否則即使呼叫 create_all()，也可能只建立空的或不完整的資料庫結構


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
