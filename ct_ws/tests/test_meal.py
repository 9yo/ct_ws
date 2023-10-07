from typing import Any, Dict, Tuple

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ct_ws.db.models.meal import Meal
from ct_ws.db.models.user import User


@pytest.mark.anyio
@pytest.mark.parametrize(
    "params, expected_status",
    [
        (None, status.HTTP_200_OK),
        ({"user_id": "asdas"}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"user_id": 1}, status.HTTP_200_OK),
        ({"user_id": 1, "offset": 10, "limit": 10}, status.HTTP_200_OK),
        (
            {"user_id": 1, "offset": 10, "limit": 0},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {"user_id": 1, "offset": "12341sda", "limit": 10},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_get_meals(
    client: AsyncClient,
    fastapi_app: FastAPI,
    params: Dict[str, Any],
    expected_status: int,
) -> None:
    """
    Checks Meals get endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param params: query parameters to use in the request.
    :param expected_status: expected HTTP status code from the response.
    """
    response = await client.get(
        fastapi_app.url_path_for("get_meals"),
        headers={"Authorization": "Bearer 1"},
        params=params,
    )
    assert response.status_code == expected_status


# If there are scenarios that don't fit neatly into parameterization,
# create separate test functions for them.
@pytest.mark.anyio
@pytest.mark.parametrize(
    "params, expected_status",
    [
        ({}, status.HTTP_200_OK),
        (
            {"date_gt": "2023-10-07", "date_lt": "2023-10-07"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {"date_gt": "2023-10-07 14:30:00", "date_lt": "2023-10-07 14:30:00"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {"date_gt": "2022-10-07 14:30:00", "date_lt": "2023-10-07 14:30:00"},
            status.HTTP_200_OK,
        ),
    ],
)
async def test_get_meals_date_comparison(
    client: AsyncClient,
    fastapi_app: FastAPI,
    params: Dict[str, Any],
    expected_status: int,
) -> None:
    """
    Check date comparison in the get endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param params: query parameters to use in the request.
    :param expected_status: expected HTTP status code from the response.
    """
    params = {
        "user_id": 1,
        "offset": 10,
        "limit": 10,
        **params,
    }
    response = await client.get(
        fastapi_app.url_path_for("get_meals"),
        headers={"Authorization": "Bearer 1"},
        params=params,
    )
    assert response.status_code == expected_status


@pytest.mark.anyio
async def test_add_meal(
    client: AsyncClient,
    fastapi_app: FastAPI,
    session_user: Tuple[AsyncSession, User],
) -> None:
    """
    Checks Meals post endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, user = session_user
    params = {
        "user_id": user.id,
        "name": "string",
        "description": "string",
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
    }
    response = await client.post(
        fastapi_app.url_path_for("add_meal"),
        headers={"Authorization": "Bearer 1"},
        json=params,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_meal(
    client: AsyncClient,
    fastapi_app: FastAPI,
    session_meal: Tuple[AsyncSession, Meal],
) -> None:
    """
    Checks Meals post endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, meal = session_meal
    response = await client.get(
        fastapi_app.url_path_for("get_meal", meal_id=meal.id),
        headers={"Authorization": "Bearer 1"},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_delete_meal(
    client: AsyncClient,
    fastapi_app: FastAPI,
    session_meal: Tuple[AsyncSession, Meal],
) -> None:
    """
    Checks Meals post endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, meal = session_meal
    response = await client.delete(
        fastapi_app.url_path_for("delete_meal", meal_id=meal.id),
        headers={"Authorization": "Bearer 1"},
    )
    assert response.status_code == status.HTTP_200_OK
