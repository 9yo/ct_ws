from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, Field


class Navigation(BaseModel):
    """Navigation model."""

    limit: int = Field(10, title="Limit")
    offset: int = Field(0, title="Offset")

    @classmethod
    def as_form(
        cls,
        limit: int = Form(0, title="Limit"),
        offset: int = Form(0, title="Offset"),
    ) -> "Navigation":
        """
        Pydatic model as a form.

        The as_form function is a class method that takes in the same arguments as
        the constructor, but with some additional keyword arguments. These are used to
        create an instance of the Form class from pydantic. This allows us to use this
        class as a filter for our database query.

        :param limit: int: Limit the number of results returned
        :param offset: int: Specify the offset of the first record in a result set
        :return: A navigation object
        :rtype: Navigation
        :doc-author: Trelent
        """
        return cls(limit=limit or 100, offset=offset)


class DatetimeComparisonFilter(BaseModel):
    """Datetime comparison filter model."""

    gt: datetime | None = Field(None, title="Greater than datetime")
    lt: datetime | None = Field(None, title="Less than datetime")
