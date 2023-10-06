"""User model."""

from pydantic import BaseModel, Field


class TelegramIndificator(BaseModel):
    """Model for telegram indificator."""

    telegram_id: int = Field(None, title="User Telegram ID")


class TelegramCredentials(TelegramIndificator):
    """Model for telegram credentials."""

    telegram_username: str = Field(None, title="User Telegram Username")


class TelegramCredentialsFilter(BaseModel):
    """Model for telegram credentials filter."""

    telegram_id: int = Field(..., title="User Telegram ID to filter with")
