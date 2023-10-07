"""Meal Service."""
import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ct_ws.db.models.meal import Meal
from ct_ws.web.api.base.schema import Navigation
from ct_ws.web.api.meal.schema import Meal as MealSchema
from ct_ws.web.api.meal.schema import MealFilter

logger = logging.getLogger("uvicorn")


class MealService:
    """Meal service."""

    @staticmethod
    async def get_meals(
        session: AsyncSession,
        filter_: MealFilter,
        navigation: Navigation,
    ) -> List[Meal]:
        """
        The get_meals function returns a list of meals.

        :param session: AsyncSession: Pass in the database session
        :param filter_: MealFilter | None: Filter the results
        :param navigation: Navigation | None: Paginate the results
        :return: A list of meal objects
        :rtype: List[Meal]
        :doc-author: Trelent
        """  # noqa: RST306
        query = select(Meal).offset(navigation.offset).limit(navigation.limit)

        if filter_.user_id:
            query = query.where(Meal.user_id == filter_.user_id)

        if filter_.date_gt:
            query = query.where(Meal.created_at > filter_.date_gt.replace(tzinfo=None))

        if filter_.date_lt:
            query = query.where(Meal.created_at < filter_.date_lt.replace(tzinfo=None))

        compiled_query = query.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )

        logger.info(f"MealService.get_meals.query=\n{compiled_query}")

        async with session.begin():
            return list((await session.execute(query)).scalars().all())

    @staticmethod
    async def add_meal(
        session: AsyncSession,
        meal: MealSchema,
        user_id: int,
    ) -> Meal:  # noqa: WPS211
        """
        The add_meal function adds a meal to the database.

        :param session: AsyncSession: Pass the database session to the function
        :param meal: MealSchema: Pass the meal object to the function
        :param user_id: int: Identify the user who created the meal
        :return: The meal object that was just created
        :rtype: Meal
        :doc-author: Trelent
        """
        meal_db: Meal = Meal(
            name=meal.name,
            description=meal.description,
            calories=meal.calories,
            protein=meal.protein,
            fat=meal.fat,
            carbs=meal.carbs,
            user_id=user_id,
        )
        session.add(meal_db)
        await session.commit()
        return meal_db

    @staticmethod
    async def get_meal(
        session: AsyncSession,
        meal_id: int,
    ) -> Meal:
        """
        The get_meal function returns a meal object from the database.

        :param session:
            AsyncSession: Access the database session
        :param meal_id:
            int: Specify the meal id
        :return:
            A meal object
        :rtype:
            Meal
        :raises HTTPException:
            If the meal is not found
        :doc-author:
            Trelent
        """  # noqa: DAR003
        query = select(Meal).where(Meal.id == meal_id)
        meal: Meal | None = (await session.execute(query)).scalar_one_or_none()

        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meal with id {meal_id} not found",
            )
        return meal

    @staticmethod
    async def delete_meal(
        session: AsyncSession,
        meal_id: int,
    ) -> Meal:
        """
        The delete_meal function deletes a meal from the database.

        :param session: AsyncSession: Pass the session of the request
        :param meal_id: int: Identify the meal to be deleted
        :return: The meal that was deleted
        :rtype: Meal
        :doc-author: Trelent
        """
        meal = await MealService.get_meal(session, meal_id)
        meal.is_deleted = True
        await session.commit()
        return meal
