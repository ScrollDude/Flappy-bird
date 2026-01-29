from sqlalchemy import select
from src.infrastructure.repositories.base_repository import BaseRepository
from src.infrastructure.models.db.game_session import GameSession
from src.infrastructure.models.db.death_reason import DeathReason
from src.core.database import session_maker


class DeathReasonRepository(BaseRepository):
    def __init__(self, model: GameSession):
        super().__init__(
            model=model,
        )

    def check_for_reasoning(self, death_reason: str):
        with session_maker() as session:
            query = select(DeathReason.id).filter_by(name=death_reason)
            result = session.execute(query)
            return result.scalars().first()


death_reason_repository = DeathReasonRepository(model=DeathReason)
