"""User service."""
from decimal import Decimal
from typing import List

from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from ct_ws.db.models.user import User
from ct_ws.db.models.user_body_parameters import UserBodyParameters
from ct_ws.db.models.user_telegram_credentials import UserTelegramCredentials


class UserService:
    """User service."""

    @staticmethod
    async def create_user(
        session: AsyncSession,
        username: str | None = None,
        email: str | None = None,
    ) -> User:
        """
        The create_user function creates a new user in the database.

        :param session: AsyncSession: Pass the session of the request to the function
        :param username: str | None: Specify the username of the user
        :param email: str | None: Create the email field in the user class
        :return: A user object
        :rtype: User
        :doc-author: Trelent
        """
        user: User = User(
            username=username,
            email=email,
        )
        session.add(user)
        await session.flush([user])
        return user

    @staticmethod
    async def add_body_parameters(
        session: AsyncSession,
        user_id: int,
        height_cm: float,
        weight_kg: float,
        age_yr: int,
    ) -> None:
        """
        The add_body_parameters function adds a user's body parameters to the database.

        :param session: AsyncSession: Pass the database session to the function
        :param user_id: int: Identify the user
        :param height_cm: float: Set the height of a user in centimeters
        :param weight_kg: float: Set the weight of the user in kilograms
        :param age_yr: int: Set the age of the user
        :rtype: NoneType
        :doc-author: Trelent
        """
        user: User = await UserService.get_user(
            session=session,
            user_id=user_id,
        )
        body_params = UserBodyParameters(
            height_cm=Decimal(height_cm),
            weight_kg=Decimal(weight_kg),
            age_yr=age_yr,
            user_id=user.id,
        )
        session.add(body_params)

    @staticmethod
    async def get_user(
        session: AsyncSession,
        user_id: int | None = None,
        tg_id: int | None = None,
        with_body_params: bool = False,
        with_telegram_credentials: bool = False,
    ) -> User:
        """
        The get_user function is used to retrieve a user from the database.

        :param session: AsyncSession: Pass the session of the current
        :param user_id: int | None: Specify the user_id of the user
        :param tg_id: int | None: Specify the telegram id of the user
        :param with_body_params: bool: Specify if the body parameters should be included
        :param with_telegram_credentials: bool:
            Specify if the telegram credentials should be included
        :return: A user object
        :rtype: User
        :raises HTTPException: If the user is not found
        :raises HTTPException: If neither user_id or tg_id is specified
        :doc-author: Trelent
        """  # noqa: DAR003
        query = select(User)

        if user_id:
            query = query.where(User.id == user_id)

        if tg_id:
            query = query.join(User.telegram_credentials).filter(
                UserTelegramCredentials.telegram_id == tg_id,
            )

        if with_body_params:
            query = query.options(joinedload(User.user_body_parameters))

        if with_telegram_credentials:
            query = query.options(joinedload(User.telegram_credentials))

        user = (await session.execute(query)).unique().scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @staticmethod
    async def get_users(
        session: AsyncSession,
        with_body_params: bool = False,
        with_telegram_credentials: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> List[User]:
        """
        The get_users function returns a list of users.

        :param session: AsyncSession: Pass the session of the request to this function
        :param with_body_params: bool: Specify if the body parameters should be included
        :param with_telegram_credentials: bool:
            Specify if the telegram credentials should be included
        :param limit: int: Limit the number of users returned
        :param offset: int: Specify the number of rows to skip
        :return: A list of user objects
        :rtype: List[User]
        :doc-author: Trelent
        """
        query = select(User).offset(offset).limit(limit)

        if with_body_params:
            query = query.options(joinedload(User.user_body_parameters))

        if with_telegram_credentials:
            query = query.options(joinedload(User.telegram_credentials))

        return list(
            ((await session.execute(query)).unique().scalars().all()),
        )
