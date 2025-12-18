from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class DeathReason(Base):
    __tablename__ = "death_reason"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
