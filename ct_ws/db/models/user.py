"""User model."""
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ct_ws.db.base import Base
from ct_ws.db.models.meal import Meal
from ct_ws.db.models.user_body_parameters import UserBodyParameters
from ct_ws.db.models.user_telegram_credentials import UserTelegramCredentials


class User(Base):
    """User model."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    meals: Mapped[Meal] = relationship(back_populates="user")
    user_body_parameters: Mapped[List[UserBodyParameters]] = relationship(
        back_populates="user",
    )
    telegram_credentials: Mapped[UserTelegramCredentials] = relationship(
        back_populates="user",
    )
