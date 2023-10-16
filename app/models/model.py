from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from app.db.database import Base
from app.schemas.companies import CompanySchema
from app.schemas.invitations import InvitationSchema
from app.schemas.members import MemberSchema
from app.schemas.requests import RequestSchema
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
            hashed_password=self.hashed_password,
            user_firstname=self.user_firstname,
            user_lastname=self.user_lastname,
            user_status=self.user_status,
            user_city=self.user_city,
            user_phone=self.user_phone,
            user_avatar=self.user_avatar,
            is_superuser=self.is_superuser,
        )


class Company(Base):
    __tablename__ = "Company"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("User.id"))
    company_name = Column(String, nullable=False)
    company_title = Column(String, nullable=False)
    company_description = Column(String, nullable=False)
    company_city = Column(String, nullable=True)
    company_phone = Column(String, nullable=True)
    company_links = Column(String, nullable=True)
    company_avatar = Column(String, nullable=True)
    is_visible: bool = Column(Boolean, default=False, nullable=False)

    def to_read_model(self) -> CompanySchema:
        return CompanySchema(
            id=self.id,
            owner_id=self.owner_id,
            company_name=self.company_name,
            company_title=self.company_title,
            company_description=self.company_description,
            company_city=self.company_city,
            company_phone=self.company_phone,
            company_links=self.company_links,
            company_avatar=self.company_avatar,
            is_visible=self.is_visible,
        )


# action_id, user_id, company_id, action


class Invitation(Base):
    __tablename__ = "Invitation"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("User.id"))
    user_id = Column(Integer, ForeignKey("User.id"))
    company_id = Column(Integer, ForeignKey("Company.id"))
    is_accepted: bool = Column(Boolean, default=None)

    def to_read_model(self) -> InvitationSchema:
        return InvitationSchema(
            id=self.id,
            sender_id=self.sender_id,
            user_id=self.user_id,
            company_id=self.company_id,
            is_accepted=self.is_accepted,
        )


class Request(Base):
    __tablename__ = "Request"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("User.id"))
    company_id = Column(Integer, ForeignKey("Company.id"))
    is_accepted: bool = Column(Boolean, default=None)

    def to_read_model(self) -> RequestSchema:
        return RequestSchema(
            id=self.id,
            sender_id=self.sender_id,
            company_id=self.company_id,
            is_accepted=self.is_accepted,
        )


class Member(Base):
    __tablename__ = "Member"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    role = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("Company.id"))

    def to_read_model(self) -> MemberSchema:
        return MemberSchema(
            id=self.id,
            user_id=self.user_id,
            role=self.role,
            company_id=self.company_id,
        )


