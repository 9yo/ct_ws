"""UserBodyParameters model."""
from datetime import datetime

from pydantic import BaseModel, Field


class UserBodyParametersBase(BaseModel):
    """UserBodyParametersBase model."""

    weight_kg: float = Field(..., description="Weight in kilograms", gt=0)
    height_cm: float = Field(..., description="Height in centimeters", gt=0)
    age_yr: int = Field(..., description="Age in years", gt=0)


class UserBodyParameters(UserBodyParametersBase):
    """UserBodyParameters model."""

    created_at: datetime = Field(..., description="Created at")
