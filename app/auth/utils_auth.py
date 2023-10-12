import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from jose import jwt, JWTError
from fastapi import Depends

from app.auth.auth0 import VerifyToken

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
    print(payload)
    if payload is not None:
        return payload
    payload = jwt_secret_verification(credentials.credentials)
    if payload is not None:
        return payload

    return None

