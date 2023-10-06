"""User model."""
from typing import List

from pydantic import BaseModel, Field

from ct_ws.web.api.telegram_credentials.schema import (
    TelegramCredentials,
    TelegramCredentialsFilter,
)
from ct_ws.web.api.user_body_parameters.schema import UserBodyParameters


class UserIndificator(BaseModel):
    """Model for user indificator."""

    id: int = Field(..., title="User ID")


class UserBase(BaseModel):
    """Model for user base."""

    username: str | None = Field(None, title="User Username")
    email: str | None = Field(None, title="User Email")
    telegram_credentials: TelegramCredentials | None = Field(
        None,
        title="User Telegram Credentials",
    )


class UserFilter(UserIndificator):
    """Model for user filter."""

    telegram_credentials: TelegramCredentialsFilter | None = Field(
        None,
        title="User Telegram Credentials",
    )

    @property
    def telegram_id(self) -> int | None:
        """
        Return the telegram id.

        :return: The telegram id.
        :rtype: int | None
        """
        if self.telegram_credentials is None:
            return None

        return self.telegram_credentials.telegram_id


class UserResponse(UserIndificator, UserBase):
    """Model for user response."""

    body_parameters_history: List[UserBodyParameters] | None = Field(
        None,
        title="User Body Parameters History",
    )

    class Config:
        """Pydantic config."""

        schema_extra = {
            "example": {
                "id": 1,
                "username": "user",
                "email": "some_user@some_domain.com",
                "telegram_credentials": {
                    "id": 123456789,
                    "username": "user",
                },
            },
        }
