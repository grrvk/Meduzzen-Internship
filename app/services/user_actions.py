from fastapi import HTTPException
from app.models.model import User
from app.repositories.companies import CompaniesRepository
from app.repositories.invitations import InvitationsRepository
from app.repositories.members import MembersRepository
from app.repositories.requests import RequestsRepository
from app.repositories.users import UsersRepository
from app.schemas.actions import UserActionCreate
from app.services.permissions import ActionsPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import ActionsValidator


class UserActionsService:
    def __init__(self, invitations_repo: AbstractRepository, requests_repo: AbstractRepository,
                 company_repo: AbstractRepository, users_repo: AbstractRepository, members_repo: AbstractRepository):
        self.invitations_repo: AbstractRepository = invitations_repo()
        self.requests_repo: AbstractRepository = requests_repo()
        self.members_repo: AbstractRepository = members_repo()
        self.actions_permissions = ActionsPermissions()
        self.validator = ActionsValidator(company_repo, users_repo, invitations_repo, members_repo)

    async def accept_invite(self, action: UserActionCreate, current_user: User):
        await self.validator.user_action_validation(action)

        invitation = await self.invitations_repo.get_one_by(user_id=current_user.id, company_id=action.company_id,
                                                            is_accepted=None)
        if not invitation:
            raise HTTPException(status_code=400, detail="user has not been invited")

        invitation_dict = invitation.model_dump()
        invitation_dict["is_accepted"] = True
        await self.invitations_repo.update_one(invitation.id, invitation_dict)

        member_dict = {"user_id": current_user.id, "role": "member", "company_id": action.company_id}
        member = await self.members_repo.create_one(member_dict)
        return member

    async def deny_invite(self, action: UserActionCreate, current_user: User):
        await self.validator.user_action_validation(action)

        invitation = await self.invitations_repo.get_one_by(user_id=current_user.id, company_id=action.company_id,
                                                            is_accepted=None)
        if not invitation:
            raise HTTPException(status_code=400, detail="user has not been invited")

        invitation_dict = invitation.model_dump()
        invitation_dict["is_accepted"] = False
        await self.invitations_repo.update_one(invitation.id, invitation_dict)

        return True

    async def send_request(self, action: UserActionCreate, current_user: User):
        company = await self.validator.user_action_validation(action)
        if company.owner_id == current_user.id:
            raise HTTPException(status_code=400, detail="user is owner of a company")
        await self.validator.user_is_not_member(current_user.id, company.id)

        request = await self.requests_repo.get_one_by(sender_id=current_user.id, company_id=action.company_id,
                                                      is_accepted=None)
        if request:
            raise HTTPException(status_code=400, detail="request has already been sent")

        request_dict = {"sender_id": current_user.id, "company_id": action.company_id}
        request = await self.requests_repo.create_one(request_dict)
        return request

    async def cancel_request(self, action: UserActionCreate, current_user: User):
        await self.validator.user_action_validation(action)

        request = await self.requests_repo.get_one_by(sender_id=current_user.id, company_id=action.company_id,
                                                      is_accepted=None)
        if not request:
            raise HTTPException(status_code=400, detail="request has not been sent")

        await self.requests_repo.delete_one(request.id)
        return True

    async def leave_company(self, action: UserActionCreate, current_user: User):
        await self.validator.user_action_validation(action)

        member = await self.members_repo.get_one_by(user_id=current_user.id, company_id=action.company_id)
        if not member:
            raise HTTPException(status_code=400, detail="no such member in the company")

        await self.members_repo.delete_one(member.id)
        return True

    async def get_all_invitations(self, current_user: User):
        return await self.invitations_repo.get_all_by(user_id=current_user.id, is_accepted=None)

    async def get_all_requests(self, current_user: User):
        return await self.requests_repo.get_all_by(sender_id=current_user.id, is_accepted=None)


class UserActionHandler:
    def __init__(self):
        self.action_service = UserActionsService(InvitationsRepository, RequestsRepository, CompaniesRepository,
                                             UsersRepository, MembersRepository)

    async def handle_action(self, action: UserActionCreate, current_user: User):
        if action.action == "Send_request":
            return await self.action_service.send_request(action, current_user)
        if action.action == "Cancel_request":
            return await self.action_service.cancel_request(action, current_user)
        if action.action == "Accept_invitation":
            return await self.action_service.accept_invite(action, current_user)
        if action.action == "Deny_invitation":
            return await self.action_service.deny_invite(action, current_user)
        if action.action == "Leave_company":
            return await self.action_service.leave_company(action, current_user)

    async def get_all_invitations(self, current_user: User):
        return await self.action_service.get_all_invitations(current_user)

    async def get_all_requests(self, current_user: User):
        return await self.action_service.get_all_requests(current_user)
