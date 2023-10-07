"""Authtentication service."""
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from ct_ws.settings import settings

security = HTTPBearer()


def auth(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:
    """
    The auth function checks if the user is authenticated.

    :param request: Request: Pass the request to the auth function
    :param credentials: HTTPAuthorizationCredentials:
        Pass the credentials to the auth function
    :return: True if the user is authenticated
    :rtype: bool
    :raises HTTPException: Raise an exception if the user is not authenticated
    """
    if credentials.credentials:
        if credentials.credentials == settings.auth_token:
            return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
