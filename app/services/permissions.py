from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.models.model import User

security = HTTPBearer()


class UserPermissions:
    def __init__(self):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")

    async def can_update_user(self, id: int, current_user: User, user_payload: dict) -> bool:
        if current_user.is_superuser:
            return True
        if current_user.id != id:
            raise self.permission_error
        for key in user_payload.keys():
            if key != "user_firstname" and key != "user_lastname" and key != "hashed_password":
                raise self.permission_error
        return True

    async def can_delete_user(self, id: int, current_user: User) -> bool:
        if current_user.id == id or current_user.is_superuser:
            return True
        raise self.permission_error

    async def can_add_user(self, current_user: User):
        if current_user.is_superuser:
            return True
        raise self.permission_error
