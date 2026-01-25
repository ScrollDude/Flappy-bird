from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from src.infrastructure.models.db.death_reason import DeathReason
from src.infrastructure.repositories.base_repository import BaseRepository
from src.infrastructure.models.db.game_session import GameSession
from src.core.database import session_maker


class GameSessionRepository(BaseRepository):
    def get_games_sessions(self):
        with session_maker() as session:
            query = select(GameSession)
            result = session.execute(query)
            return result.scalars().all()

    def get_top_scores(self):
        with session_maker() as session:
            query = select(func.max(GameSession.score))
            result = session.execute(query)
            return result.scalar_one()

    def get_best_session(self):
        with session_maker() as session:
            query = select(GameSession).order_by(GameSession.score.desc()).limit(1)
            result = session.execute(query)
            return result.scalars().first()


game_session_repository = GameSessionRepository(model=GameSession)
