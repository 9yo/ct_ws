from typing import Any, AsyncGenerator, Tuple

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ct_ws.db.dependencies import get_db_session
from ct_ws.db.models.meal import Meal
from ct_ws.db.models.user import User
from ct_ws.db.models.user_telegram_credentials import UserTelegramCredentials
from ct_ws.db.utils import create_database, drop_database
from ct_ws.settings import settings
from ct_ws.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from ct_ws.db.meta import meta  # noqa: WPS433
    from ct_ws.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test",
        headers={
            "Authorization": f"Bearer {settings.auth_token}",
        },
    ) as ac:
        yield ac


@pytest.fixture
async def session_user(
    dbsession: AsyncSession,
) -> AsyncGenerator[Tuple[AsyncSession, User], None]:
    """
    Fixture that creates a user in the database.

    The session_user function is a fixture that creates a new database session and adds
    a user to the database. It then yields the session and user instance so that they
    can be used in tests. When all of the tests are finished, it will close out the
    session.

    :param dbsession: AsyncSession: Pass the database session to the function
    :yield: A tuple containing an asyncsession and a user
    :rtype: Tuple[AsyncSession, User]
    :doc-author: Trelent
    """
    user_instance = User(username="test_user")
    dbsession.add(user_instance)
    await dbsession.flush([user_instance])

    telegram_credentials = UserTelegramCredentials(
        telegram_id=123456789,
        telegram_username="test_user",
        user_id=user_instance.id,
    )

    dbsession.add(telegram_credentials)
    await dbsession.flush([telegram_credentials])

    await dbsession.commit()

    yield dbsession, user_instance


@pytest.fixture
async def session_meal(
    session_user: Tuple[AsyncSession, User],
) -> AsyncGenerator[Tuple[AsyncSession, Meal], None]:
    """
    Fixture that creates a meal in the database.

    The session_meal function is a fixture that creates a new meal for the user
    and returns it. It also yields the session and meal to be used in tests.

    :param session_user: Tuple[AsyncSession, User]:
        Pass in the user object that was created
    :yield: A tuple of the session and meal
    :rtype: Tuple[AsyncSession, Meal]
    :doc-author: Trelent
    """
    session, user = session_user
    meal: Meal = Meal(
        user_id=user.id,
        name="Test Meal",
        description="Test Description",
        calories=100,
        protein=10,
        fat=10,
        carbs=10,
    )

    session.add(meal)
    await session.commit()
    yield session, meal
