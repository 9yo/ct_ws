"""Meal model."""

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ct_ws.db.base import Base
from ct_ws.db.models.user import User


class Meal(Base):
    """Meal model."""

    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        comment="Name of the meal",
    )
    description: Mapped[str | None] = mapped_column(
        comment="Description of the meal",
    )
    calories: Mapped[int] = mapped_column(
        comment="Calories of the meal",
    )
    protein: Mapped[float] = mapped_column(
        comment="Protein of the meal",
    )
    fat: Mapped[float] = mapped_column(
        comment="Fat of the meal",
    )
    carbs: Mapped[float] = mapped_column(
        comment="Carbs of the meal",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        comment="User ID of the meal",
    )
    user: Mapped[User] = relationship(back_populates="meals")

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        comment="Is deleted flag of the meal",
    )
    created_at: Mapped[datetime] = mapped_column(
        comment="Created at timestamp of the meal",
        default=datetime.utcnow,
    )
