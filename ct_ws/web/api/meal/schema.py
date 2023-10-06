"""Meal API models."""
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, Field

from ct_ws.web.api.base.schema import DatetimeComparisonFilter


class Meal(BaseModel):
    """Meal model."""

    name: str = Field(..., title="Meal Name")
    description: str = Field(..., title="Meal Description")
    calories: int = Field(..., title="Meal Calories")
    protein: float = Field(..., title="Meal Protein Grams")
    fat: float = Field(..., title="Meal Fat Grams")
    carbs: float = Field(..., title="Meal Carbs Grams")
    created_at: datetime = Field(..., title="Meal Created At")
    user_id: int = Field(..., title="User ID")


class MealResponse(Meal):
    """Meal response model."""

    id: int = Field(..., title="Meal ID")


class MealFilter(BaseModel):
    """Meal filter model."""

    user_id: int | None = Field(None, title="User ID")
    date: DatetimeComparisonFilter | None = Field(None, title="Date")

    @property
    def date_lt(self) -> datetime | None:
        """
        Date less than.

        :return: The date less than.
        :rtype: datetime | None
        """
        if self.date:
            return self.date.lt
        return None

    @property
    def date_gt(self) -> datetime | None:
        """
        Date less than.

        :return: The date greater than.
        :rtype: datetime | None
        """
        if self.date:
            return self.date.gt
        return None

    @classmethod
    def as_form(
        cls,
        user_id: int | None = Form(None, title="User ID"),
        date_gt: datetime | None = Form(None, title="Greater than timestamp"),
        date_lt: datetime | None = Form(None, title="Less than timestamp"),
    ) -> "MealFilter":
        """
        Pydatic model as a form.

        The as_form function is a class method that takes in the same arguments as
        the constructor, but with some additional keyword arguments. These are used to
        create an instance of the Form class from pydantic. This allows us to use this
        class as a filter for our database query.

        :param user_id: int | None: Specify that the user_id field is an integer or none
        :param date_gt: datetime | None: Specify that the parameter is optional
        :param date_lt: datetime | None: Specify that the date_lt parameter is optional
        :return: A mealfilter object, which is a dataclass
        :rtype: MealFilter
        :doc-author: Trelent
        """
        return cls(
            user_id=user_id,
            date=DatetimeComparisonFilter(gt=date_gt, lt=date_lt),
        )
