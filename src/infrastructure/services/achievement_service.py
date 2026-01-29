from typing import Optional
from src.infrastructure.repositories import achievement_repository
from src.infrastructure.models.db.death_reason import DeathReason
from src.infrastructure.repositories.achievement_repository import AchievementRepository


class AchievementService:
    def __init__(self, repo: AchievementRepository):
        self.repo = repo

    def check_and_update(self, achievement_id: int) -> Optional[DeathReason]:
        return self.repo.check_and_update(achievement_id)

    def get_all_completed(self) -> Optional[list[DeathReason]]:
        return self.repo.get_all_completed()


achievement_service = AchievementService(repo=achievement_repository)
