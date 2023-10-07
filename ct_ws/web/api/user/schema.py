"""User model."""
from typing import Any, Dict, List

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pydantic.class_validators import root_validator
from starlette import status

from ct_ws.web.api.telegram_credentials.schema import TelegramCredentials
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


class UserFilter(BaseModel):
    """Model for user filter."""

    id: int | None = Field(None, title="User ID")
    telegram_id: int | None = Field(None, title="User Telegram ID to filter with")

    @root_validator
    @classmethod
    def check_id_or_telegram_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if id or telegram_id is provided.

        :param values: Dict[str, Any]: Values to validate
        :return: The validated values
        :rtype: Dict[str, Any]
        :raises HTTPException: If id or telegram_id is not provided
        """
        if not values.get("id") and not values.get("telegram_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id or telegram_id must be provided",
            )
        return values


class UserResponse(UserIndificator, UserBase):
    """Model for user response."""

    body_parameters_history: List[UserBodyParameters] | None = Field(
        None,
        title="User Body Parameters History",
    )

    class Config:
        """Pydantic config."""

        orm_mode = True
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
