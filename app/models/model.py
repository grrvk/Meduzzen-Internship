from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DateTime
from app.db.database import Base
import pytz
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.schemas.schema import UserSchema


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    user_firstname = Column(String, nullable=False)
    user_lastname = Column(String, nullable=False)
    user_status = Column(Boolean, default=True, nullable=True)
    user_city = Column(String, nullable=True)
    user_phone = Column(String, nullable=True)
    user_avatar = Column(String, nullable=True)
    hashed_password: str = Column(String, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            user_email=self.user_email,
            user_firstname=self.user_firstname,
            user_lastname=self.user_lastname,
            user_status=self.user_status,
            user_city=self.user_city,
            user_phone=self.user_phone,
            user_avatar=self.user_avatar,
        )
