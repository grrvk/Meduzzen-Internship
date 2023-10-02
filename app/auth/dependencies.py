import os
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.services.dependencies import users_service
from app.services.users import UserService


ALGORITHM = os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


oath2_bearer = OAuth2PasswordBearer(
    tokenUrl="token",
)


async def get_current_user(token: Annotated[str, Depends(oath2_bearer)],
                           user_service: Annotated[UserService, Depends(users_service)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user_by_email(email)

    if user is None:
        raise credentials_exception
    return user


async def get_user_info_jwt(token: Annotated[str, Depends(oath2_bearer)],
                           user_service: Annotated[UserService, Depends(users_service)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None

    user = await user_service.get_user_by_email(email)

    if user is None:
        return None
    return user


