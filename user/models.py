from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Float
from sqlalchemy.orm import declarative_base

from core.settings import BaseMixinIntegerID

UserBase = declarative_base(cls=BaseMixinIntegerID)


class Role(UserBase):
    __tablename__ = 'role'
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(SQLAlchemyBaseUserTable[int], UserBase):
    pass