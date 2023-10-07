from typing import Dict, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ct_ws.db.dependencies import get_db_session
from ct_ws.db.models.user import User
from ct_ws.services.telegram_credentials import TelegramCredentialsService
from ct_ws.services.user import UserService
from ct_ws.web.api.base.schema import Navigation
from ct_ws.web.api.telegram_credentials.schema import TelegramCredentials
from ct_ws.web.api.user.schema import UserBase, UserFilter, UserResponse
from ct_ws.web.api.user_body_parameters.schema import UserBodyParametersBase

router = APIRouter()


@router.post("")
async def create_user(
    user: UserBase,
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    """
    The create_user function creates a new user in the database.

    :param user: UserBase: Pass the user object to the create_user function
    :param session: AsyncSession: Pass the session to the service layer
    :return: A userresponse object.
    :rtype: UserResponse
    :doc-author: Trelent
    """
    user_db: "User" = await UserService.create_user(
        session=session,
        username=user.username,
        email=user.email,
    )
    tcr = None
    if user.telegram_credentials:
        user_db.telegram_credentials = (
            await TelegramCredentialsService.create_telegram_credentials(
                session=session,
                user_id=user_db.id,
                telegram_id=user.telegram_credentials.telegram_id,
                telegram_username=user.telegram_credentials.telegram_username,
            )
        )
        tcr = TelegramCredentials.from_orm(user_db.telegram_credentials)

    await session.commit()
    return UserResponse(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        telegram_credentials=tcr,
        body_parameters_history=[],
    )


@router.post("/{user_id}/body_parameters")
async def add_body_parameters(
    user_id: int,
    body_parameters: UserBodyParametersBase = Body(..., title="User Body Parameters"),
    session: AsyncSession = Depends(get_db_session),
) -> Dict[str, str]:
    """
    The add_body_parameters function adds body parameters to a user.

    :param user_id:
        int: Identify the user
    :param body_parameters:
        UserBodyParametersBase: Define the type of data that is expected to be passed in
    :param session: AsyncSession: Pass the session object to the service
    :returns: A dictionary with the key "status" and value "ok"
    :rtype: Dict[str, str]
    :doc-author: Trelent
    """
    await UserService.add_body_parameters(
        session=session,
        user_id=user_id,
        height_cm=body_parameters.height_cm,
        weight_kg=body_parameters.weight_kg,
        age_yr=body_parameters.age_yr,
    )

    await session.commit()

    return {"status": "ok"}


@router.get("")
async def get_users(
    navigation: Navigation = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> List[UserResponse]:
    """
    The get_users function returns a list of users.

    :param navigation:
        Navigation | None: Receive the limit and offset parameters from the request
    :param session: AsyncSession: Pass the session object to the function
    :return: A list of userresponse objects
    :rtype: List[UserResponse]
    :doc-author: Trelent
    """
    limit = 100
    offset = 0
    if navigation:
        limit = navigation.limit
        offset = navigation.offset
    users = await UserService.get_users(
        session=session,
        with_body_params=True,
        with_telegram_credentials=True,
        limit=limit,
        offset=offset,
    )

    return [UserResponse.from_orm(user) for user in users]


@router.get("/")
async def get_user(
    filter_: UserFilter = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    """
    The get_user function returns a user object.

    :param filter_: UserFilter | None: Filter the users
    :param session: AsyncSession: Get the session object
    :return: A userresponse object
    :rtype: UserResponse
    :doc-author: Trelent
    """  # noqa: RST306
    user_id = None
    tg_id = None
    if filter_:
        user_id = filter_.id
        tg_id = filter_.telegram_id
    user_db = await UserService.get_user(
        session=session,
        user_id=user_id,
        tg_id=tg_id,
        with_body_params=True,
        with_telegram_credentials=True,
    )

    return UserResponse.from_orm(user_db)
