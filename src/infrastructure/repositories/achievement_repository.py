from abc import ABC, abstractmethod

from src.infrastructure.repositories.base_repository import BaseRepository
from src.infrastructure.models.db.game_session import GameSession


class AchievementAbstractRepository(ABC):
    @abstractmethod
    def get_games_sessions(self) -> list[GameSession]: ...

    @abstractmethod
    def get_top_scores(self) -> list[GameSession]: ...

    @abstractmethod
    def get_recent_games(self) -> list[GameSession]: ...


class AchievementRepository(BaseRepository, AchievementAbstractRepository):
    def __init__(self, model: GameSession):
        super().__init__(
            model=model,
        )
