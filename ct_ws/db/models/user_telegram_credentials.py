"""UserTelegramCredential model."""
from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ct_ws.db.base import Base
from ct_ws.db.models.user import User
from ct_ws.web.api.telegram_credentials.schema import TelegramCredentials


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

    def to_response(self, api_version: Literal[1] = 1) -> TelegramCredentials:
        """
        Converts UserTelegramCredentials to TelegramCredentials.

        The to_response function is used to convert the User object into a dictionary
        that can be sent as JSON. This function is called by the API when it needs to
        send a response back to the client. The function takes an optional
        api_parameter, which allows us to specify what version of our API we are using.
        We will use this parameter in future versions of our API, when we want to change
        how data is returned.

        :param api_version: Literal[1]: Specify the version of the api
        :return: Pydantic model
        :rtype: TelegramCredentials
        :doc-author: Trelent
        """
        if api_version == 1:
            return TelegramCredentials(
                telegram_id=self.telegram_id,
                telegram_username=self.telegram_username,
            )
