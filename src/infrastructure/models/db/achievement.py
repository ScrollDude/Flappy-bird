from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class Achievement(Base):
    __tablename__ = "achievement"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    is_complete: Mapped[bool] = mapped_column(default=False)
