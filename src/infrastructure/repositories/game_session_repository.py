from abc import ABC, abstractmethod

from src.infrastructure.models.db.game_session import GameSession

class GameSessionAbstractRepository(ABC):
    @abstractmethod
    def add(self): ...

    @abstractmethod
    def get_games_sessions(self) -> list[GameSession]: ...

    @abstractmethod
    def get_top_scores(self) -> list[GameSession]: ...

    @abstractmethod
    def get_recent_games(self) -> list[GameSession]: ...


class GameSessionRepository(GameSessionAbstractRepository):
    def __init__(self, model: GameSession):
        self.model = model
