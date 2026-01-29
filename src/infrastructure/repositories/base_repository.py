from sqlalchemy import insert
from src.core.database import Base
from src.core.database import session_maker


class BaseRepository:
    def __init__(self, model: Base):
        self.model = model

    def add(self, **params) -> None:
        with session_maker() as session:
            query = insert(self.model).values(params)
            session.execute(query)
            session.commit()
