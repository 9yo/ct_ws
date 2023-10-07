from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ct_ws.db.dependencies import get_db_session
from ct_ws.db.models.meal import Meal as MealDB
from ct_ws.services.meal import MealService
from ct_ws.services.user import UserService
from ct_ws.web.api.base.schema import Navigation
from ct_ws.web.api.meal.schema import Meal as MealSchema
from ct_ws.web.api.meal.schema import MealFilter, MealResponse

router = APIRouter()


@router.get("/", response_model=List[MealResponse])
async def get_meals(
    filter_: MealFilter = Depends(),
    navigation: Navigation = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> List[MealResponse]:
    """
    The get_meals function returns a list of meals.

    :param filter_: MealFilter | None: Filter the meals by user_id and date
    :param navigation:
        Navigation | None: Pass the limit and offset values to the get_meals function
    :param session: AsyncSession: Pass the session to the service layer
    :return: A list of mealresponse objects
    :rtype: List[MealResponse]
    :doc-author: Trelent
    """  # noqa: RST306
    meals: List[MealDB] = await MealService.get_meals(
        filter_=filter_,
        navigation=navigation,
        session=session,
    )

    return [MealResponse.from_orm(meal) for meal in meals]


@router.post("/", response_model=MealResponse)
async def add_meal(
    meal: MealSchema,
    session: AsyncSession = Depends(get_db_session),
) -> MealResponse:
    """
    The add_meal function adds a meal to the database.

    :param meal: MealBase: Get the data from the request body
    :param session: AsyncSession: Get the user_id from the request
    :return: A mealresponse object, which is defined in the models
    :rtype: MealResponse
    :doc-author: Trelent
    """
    user = await UserService.get_user(
        session=session,
        user_id=meal.user_id,
    )

    meal_db: MealDB = await MealService.add_meal(
        session=session,
        meal=meal,
        user_id=user.id,
    )

    return MealResponse.from_orm(meal_db)


@router.get("/{meal_id}/", response_model=MealResponse, name="get_meal")
async def get_meal(
    meal_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> MealResponse:
    """
    The get_meal function is used to retrieve a single meal from the database.

    :param meal_id: int: Specify the meal id to be retrieved
    :param session: AsyncSession: Get the session object that is passed to the function
    :return: A mealresponse object
    :rtype: MealResponse
    :doc-author: Trelent
    """
    meal_db: MealDB = await MealService.get_meal(
        session=session,
        meal_id=meal_id,
    )

    return MealResponse.from_orm(meal_db)


@router.delete("/{meal_id}/", response_model=MealResponse, name="delete_meal")
async def delete_meal(
    meal_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> MealResponse:
    """
    The delete_meal function deletes a meal from the database.

    :param meal_id: int: Identify the meal that we want to delete
    :param session: AsyncSession: Get the current session of the request
    :return: A mealresponse object
    :rtype: MealResponse
    :doc-author: Trelent
    """
    meal_db: MealDB = await MealService.delete_meal(
        session=session,
        meal_id=meal_id,
    )

    return MealResponse.from_orm(meal_db)
