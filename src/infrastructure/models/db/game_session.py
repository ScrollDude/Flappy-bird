from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.infrastructure.models.db.death_reason import DeathReason


class GameSession(Base):
    __tablename__ = "game_session"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column()
    level_reached: Mapped[int] = mapped_column()
    distance: Mapped[int] = mapped_column()
    duration_seconds: Mapped[int] = mapped_column()
    powerup_types_count: Mapped[int] = mapped_column()
    pipes_passed: Mapped[int] = mapped_column()
    # death_reason_id: Mapped[int] = mapped_column(ForeignKey("death_reason.id"))
    # death_reason: Mapped[DeathReason] = relationship()
