from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.sql import func

from fpgen.orm.sqlalchemy.base import Base


class BaseModel:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BaseIDModel(Base, BaseModel):
    __abstract__ = True
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
