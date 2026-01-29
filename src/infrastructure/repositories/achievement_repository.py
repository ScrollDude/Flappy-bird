from sqlalchemy import select
from src.infrastructure.repositories.base_repository import BaseRepository
from src.infrastructure.models.db.game_session import GameSession
from src.infrastructure.models.db.achievement import Achievement
from src.core.database import session_maker


class AchievementRepository(BaseRepository):
    def __init__(self, model: GameSession):
        super().__init__(
            model=model,
        )

    def check_and_update(self, id: int):
        with session_maker() as session:
            query = select(Achievement).filter_by(id=id)

            achievement = session.execute(query)
            achievement = achievement.scalars().first()

            if not achievement.is_complete:
                achievement.is_complete = True

            session.commit()

    def get_all_completed(self):
        with session_maker() as session:
            query = select(Achievement).filter(Achievement.is_complete == True)
            result = session.execute(query)

            return result.scalars().all()


achievement_repository = AchievementRepository(model=Achievement)
