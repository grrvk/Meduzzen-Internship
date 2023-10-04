import secrets
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from jose import jwt, JWTError
from fastapi import Depends, HTTPException

from app.auth.auth0 import VerifyToken
from app.schemas.schema import UserSignUpRequest
from app.services.users import UserService

ALGORITHM = os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
AUTH0_DOMAIN = os.environ['DOMAIN']
AUTH0_AUDIENCE = os.environ['API_AUDIENCE']
AUTH0_ALG = os.environ['AUTH0_ALGORITHM']
ISSUER = os.environ['ISSUER']

security = HTTPBearer()


def auth0_verification(credentials: str):
    payload = VerifyToken(credentials).verify()
    if payload.get("status"):
        return None
    return payload


def jwt_secret_verification(credentials: str):
    try:
        payload = jwt.decode(credentials, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def check_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = auth0_verification(credentials.credentials)
    if payload is not None:
        return payload
    payload = jwt_secret_verification(credentials.credentials)
    if payload is not None:
        return payload

    return None


async def get_user_by_payload(payload: dict, user_service: UserService):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if payload is None:
        raise credentials_exception

    scope = payload.get("scope")
    if scope == "openid profile email":
        email = payload.get("user_email")
        try:
            user = await user_service.get_user_by_email(email)
            return user.id
        except:
            added_user = UserSignUpRequest(user_email=email, hashed_password=secrets.token_urlsafe(15),
                                           user_firstname="string", user_lastname="string"
                                           )
            user_id = await user_service.add_user(added_user)
            return user_id
    if scope == "secret jwt":
        email = payload.get("sub")
        user = await user_service.get_user_by_email(email)
        return user.id
