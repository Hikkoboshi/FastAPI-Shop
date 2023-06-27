import re
import os
from dotenv import load_dotenv

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr

from pydantic import BaseModel

load_dotenv()


class BaseSchemaModel(BaseModel):
    class Config:
        orm_mode = True


class BaseMixinIntegerID(object):
    @declared_attr
    def __tablename__(cls):
        class_name = [name.lower() for name in re.findall('[A-Z][^A-Z]*', cls.__name__)]
        return '_'.join(class_name)

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=BaseMixinIntegerID)

# Database settings
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

