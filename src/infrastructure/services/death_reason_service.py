from typing import Optional
from src.infrastructure.repositories import death_reason_repository
from src.infrastructure.models.db.death_reason import DeathReason
from src.infrastructure.repositories.death_reason_repository import DeathReasonRepository


class DeathReasonService:
    def __init__(self, repo: DeathReasonRepository):
        self.repo = repo

    def check_for_reasoning(self, death_reason_id: str) -> Optional[DeathReason]:
        return self.repo.check_for_reasoning(death_reason_id)


death_reason_service = DeathReasonService(repo=death_reason_repository)