from pydantic import BaseModel, Field


class Navigation(BaseModel):
    """Navigation model."""

    limit: int = Field(100, title="Limit", gt=0, le=100)
    offset: int = Field(0, title="Offset")
