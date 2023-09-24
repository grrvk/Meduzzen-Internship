from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DateTime
from app.db.database import Base

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    user_firstname = Column(String, nullable=False)
    user_lastname = Column(String, nullable=False)
    user_status = Column(Boolean, default=True, nullable=True)
    user_city = Column(String, nullable=True)
    user_phone = Column(String, nullable=True)
    user_avatar = Column(String, nullable=True)
    hashed_password: str = Column(String, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


