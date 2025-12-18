from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase): ...
