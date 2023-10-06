"""UserBodyParameters model."""
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ct_ws.db.base import Base
from ct_ws.db.models.user import User


class UserBodyParameters(Base):
    """UserBodyParameters model."""

    __tablename__ = "user_body_parameters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user: Mapped[User] = mapped_column(back_populates="user_body_parameters")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        comment="User ID of the user body parameters",
    )
    weight_kg: Mapped[float] = mapped_column(
        comment="Weight in kilograms",
    )
    height_cm: Mapped[float] = mapped_column(
        comment="Height in centimeters",
    )
    age_yr: Mapped[int] = mapped_column(
        comment="Age in years",
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        comment="Created at timestamp of the user body parameters",
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
        comment="Deleted at timestamp of the user body parameters",
    )
