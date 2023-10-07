"""User api tests."""
from typing import Tuple

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ct_ws.db.models.user import User


@pytest.mark.anyio
async def test_create_user(
    auth_client: AsyncClient,
    fastapi_app: FastAPI,
    session_user: Tuple[AsyncSession, User],
) -> None:
    """
    Checks Users post endpoint.

    :param auth_client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    response = await auth_client.post(
        fastapi_app.url_path_for("create_user"),
        json={
            "username": "tester1",
            "email": "tester1@ct_ws@mail.com",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    response = await auth_client.post(
        fastapi_app.url_path_for("create_user"),
        json={
            "username": "tester2",
            "email": "tester2@ct_ws@mail.com",
            "telegram_credentials": {
                "telegram_id": 2342342,
                "telegram_username": "alexader_tester2",
            },
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_add_body_parameters(
    auth_client: AsyncClient,
    fastapi_app: FastAPI,
    session_user: Tuple[AsyncSession, User],
) -> None:
    """
    Checks Users post endpoint.

    :param auth_client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, user = session_user
    response = await auth_client.post(
        fastapi_app.url_path_for("add_body_parameters", user_id=user.id),
        json={
            "weight_kg": 1,
            "height_cm": 1,
            "age_yr": 1,
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_users(
    auth_client: AsyncClient,
    fastapi_app: FastAPI,
    session_user: Tuple[AsyncSession, User],
) -> None:
    """
    Checks Users post endpoint.

    :param auth_client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, user = session_user
    response = await auth_client.get(
        fastapi_app.url_path_for("get_users"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert user.username in response.json()[0]["username"]


@pytest.mark.anyio
async def test_get_user(
    auth_client: AsyncClient,
    fastapi_app: FastAPI,
    session_user: Tuple[AsyncSession, User],
) -> None:
    """
    Checks Users post endpoint.

    :param auth_client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    session, user = session_user
    response = await auth_client.get(
        fastapi_app.url_path_for("get_user"),
        params={},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    session, user = session_user
    response = await auth_client.get(
        fastapi_app.url_path_for("get_user"),
        params={"id": user.id},
    )
    assert response.status_code == status.HTTP_200_OK
    assert user.username in response.json()["username"]

    response = await auth_client.get(
        fastapi_app.url_path_for("get_user"),
        params={"telegram_id": user.telegram_credentials.telegram_id},
    )
    resp = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert (
        user.telegram_credentials.telegram_id
        == resp["telegram_credentials"]["telegram_id"]
    )
