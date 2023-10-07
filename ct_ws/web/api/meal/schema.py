"""Meal API models."""
from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException
from pydantic import BaseModel, Field
from pydantic.class_validators import root_validator
from starlette import status


class Meal(BaseModel):
    """Meal model."""

    user_id: int = Field(..., title="User ID", gt=0)
    name: str = Field(..., title="Meal Name")
    description: str = Field(..., title="Meal Description")
    calories: int = Field(..., title="Meal Calories")
    protein: float = Field(..., title="Meal Protein Grams")
    fat: float = Field(..., title="Meal Fat Grams")
    carbs: float = Field(..., title="Meal Carbs Grams")


class MealResponse(Meal, orm_mode=True):
    """Meal response model."""

    id: int = Field(..., title="Meal ID")


class MealFilter(BaseModel):
    """Meal filter model."""

    user_id: int | None = Field(None, title="User ID")
    date_gt: datetime | None = Field(None, title="Greater than datetime")
    date_lt: datetime | None = Field(None, title="Less than datetime")

    @root_validator
    @classmethod
    def validate_datetime_comparison_filter(
        cls,
        values: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate the datetime comparison filter.

        The validate_datetime_comparison_filter function validates the datetime
        comparison filter.

        :param values: dict: A dictionary of values
        :return: A dictionary of values
        :rtype: Dict[str, Any]
        :raises HTTPException: If date_gt is greater than or equal to date_lt
        :doc-author: Trelent
        """  # noqa: DAR003
        date_gt = values.get("date_gt")
        date_lt = values.get("date_lt")
        if date_gt and date_lt:
            if date_gt > date_lt or date_gt == date_lt:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="date_gt must be less than date_lt",
                )
        return values
