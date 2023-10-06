"""User service."""
from decimal import Decimal
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ct_ws.db.models.user import User
from ct_ws.db.models.user_body_parameters import UserBodyParameters


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
        await session.commit()
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
    ) -> User:
        """
        The get_user function is used to retrieve a user from the database.

        :param session: AsyncSession: Pass the session of the current
        :param user_id: int | None: Specify the user_id of the user
        :param tg_id: int | None: Specify the telegram id of the user
        :return: A user object
        :rtype: User
        :raises ValueError: If the user is not found
        :doc-author: Trelent
        """  # noqa: DAR003
        if not user_id and not tg_id:
            raise ValueError("user_id or tg_id must be specified")

        query = select(User)

        if user_id:
            query = query.where(User.id == user_id)

        if tg_id:
            query = query.options(joinedload(User.telegram_credentials))
            query = query.where(User.telegram_credentials.tg_id == tg_id)

        user = (await session.execute(query)).scalar_one_or_none()

        if not user:
            raise ValueError("user not found")

        return user

    @staticmethod
    async def get_users(
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> List[User]:
        """
        The get_users function returns a list of users.

        :param session: AsyncSession: Pass the session of the request to this function
        :param limit: int: Limit the number of users returned
        :param offset: int: Specify the number of rows to skip
        :return: A list of user objects
        :rtype: List[User]
        :doc-author: Trelent
        """
        return list(
            (
                (
                    await session.execute(
                        select(User).offset(offset).limit(limit),
                    )
                )
                .scalars()
                .all()
            ),
        )
