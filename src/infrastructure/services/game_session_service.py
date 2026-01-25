from src.infrastructure.repositories.game_session_repository import (
    GameSessionRepository,
)


class GameSessionService:
    def __init__(self, repository: GameSessionRepository):
        self.repository = repository

    def add(self, **args) -> None:
        self.repository.add(**args)

    def get_game_statistics(self):
        sessions = self.repository.get_games_sessions()
        if not sessions:
            return {
                "games_count": 0,
                "avg_score": 0,
                "avg_duration": 0.0,
                "avg_pipes": 0.0,
                "avg_powerups": 0.0,
                "avg_distance": 0,
                "max_score": 0,
                "max_duration": 0.0,
                "max_pipes": 0,
            }

        total_score = sum(session.score for session in sessions)
        total_duration = sum(session.duration_seconds for session in sessions)
        total_pipes = sum(session.pipes_passed for session in sessions)
        total_powerups = sum(session.powerup_types_count for session in sessions)
        total_distance = sum(session.distance for session in sessions)

        return {
            "games_count": len(sessions),
            "avg_score": round(total_score / len(sessions)),
            "avg_duration": round(total_duration / len(sessions), 1),
            "avg_pipes": round(total_pipes / len(sessions), 1),
            "avg_powerups": round(total_powerups / len(sessions), 1),
            "avg_distance": round(total_distance / len(sessions)),
            "max_score": max(session.score for session in sessions),
            "max_duration": round(
                max(session.duration_seconds for session in sessions), 1
            ),
            "max_pipes": max(session.pipes_passed for session in sessions),
        }
