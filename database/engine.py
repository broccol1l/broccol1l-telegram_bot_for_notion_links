from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase

import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv('DATABASE_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass