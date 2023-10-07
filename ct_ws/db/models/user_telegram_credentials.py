"""UserTelegramCredential model."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ct_ws.db.base import Base
from ct_ws.db.models.user import User


class UserTelegramCredentials(Base):
    """UserTelegramCredential model."""

    __tablename__ = "user_telegram_credentials"

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_username: Mapped[str] = mapped_column(
        comment="Telegram username",
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped[User] = relationship(User, back_populates="telegram_credentials")
