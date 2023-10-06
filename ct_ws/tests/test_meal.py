import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_get_meals(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks Meals get endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    response = await client.get(
        fastapi_app.url_path_for("get_meals"),
        headers={"Authorization": "Bearer 1"},
        params={"user_id": 1, "limit": 100, "offset": 0},
    )
    assert response.status_code == status.HTTP_200_OK
