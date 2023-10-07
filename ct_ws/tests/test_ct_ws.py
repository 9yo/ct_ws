import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_health(auth_client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param auth_client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
