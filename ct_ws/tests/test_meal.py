from typing import Any, Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


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
async def test_date_comparison(
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
