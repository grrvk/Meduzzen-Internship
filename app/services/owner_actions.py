from fastapi import HTTPException
from app.models.model import User
from app.repositories.companies import CompaniesRepository
from app.repositories.invitations import InvitationsRepository
from app.repositories.members import MembersRepository
from app.repositories.requests import RequestsRepository
from app.repositories.users import UsersRepository
from app.schemas.actions import OwnerActionCreate, OwnerActions
from app.services.permissions import ActionsPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import ActionsValidator


class OwnerActionsService:
    def __init__(self, invitations_repo: AbstractRepository, requests_repo: AbstractRepository,
                 company_repo: AbstractRepository, users_repo: AbstractRepository, members_repo: AbstractRepository):
        self.invitations_repo: AbstractRepository = invitations_repo()
        self.requests_repo: AbstractRepository = requests_repo()
        self.members_repo: AbstractRepository = members_repo()
        self.company_repo: AbstractRepository = company_repo()
        self.actions_permissions = ActionsPermissions()
        self.validator = ActionsValidator(company_repo, users_repo, invitations_repo, members_repo)

    async def send_invite(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        if action.user_id == current_user.id:
            raise HTTPException(status_code=400, detail="user is owner of a company")
        await self.validator.user_is_not_member(action.user_id, company.id)

        invitation = await self.invitations_repo.get_one_by(user_id=action.user_id, company_id=action.company_id,
                                                            is_accepted=None)
        if invitation:
            raise HTTPException(status_code=400, detail="user has already been invited")

        invitation_dict = {"sender_id": current_user.id, "user_id": action.user_id, "company_id": action.company_id}
        return await self.invitations_repo.create_one(invitation_dict)

    async def cancel_invite(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        invitation = await self.invitations_repo.get_one_by(user_id=action.user_id, company_id=action.company_id,
                                                            is_accepted=None)
        if not invitation:
            raise HTTPException(status_code=400, detail="user has not been invited")

        await self.invitations_repo.delete_one(invitation.id)
        return True

    async def accept_request(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        request = await self.requests_repo.get_one_by(sender_id=action.user_id, company_id=action.company_id,
                                                      is_accepted=None)
        if not request:
            raise HTTPException(status_code=400, detail="request has not been sent")

        request_dict = request.model_dump()
        request_dict["is_accepted"] = True
        await self.requests_repo.update_one(request.id, request_dict)

        member_dict = {"user_id": action.user_id, "role": "member", "company_id": action.company_id}
        return await self.members_repo.create_one(member_dict)

    async def deny_request(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        request = await self.requests_repo.get_one_by(sender_id=action.user_id, company_id=action.company_id,
                                                      is_accepted=None)
        if not request:
            raise HTTPException(status_code=400, detail="request has not been sent")

        request_dict = request.model_dump()
        request_dict["is_accepted"] = False
        await self.requests_repo.update_one(request.id, request_dict)

        return True

    async def delete_member(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        member = await self.members_repo.get_one_by(user_id=action.user_id, company_id=company.id)
        if not member:
            raise HTTPException(status_code=400, detail="no such member in the company")

        await self.members_repo.delete_one(member.id)
        return True

    async def add_admin(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        member = await self.members_repo.get_one_by(user_id=action.user_id, company_id=company.id)
        if not member:
            raise HTTPException(status_code=400, detail="no such member in the company")

        member_dict = member.model_dump()
        if member_dict["role"] == "admin":
            raise HTTPException(status_code=400, detail="member is already admin")
        member_dict["role"] = "admin"
        await self.members_repo.update_one(member.id, member_dict)
        return True

    async def remove_admin(self, action: OwnerActionCreate, current_user: User):
        company = await self.validator.owner_action_validation(action)
        await self.actions_permissions.is_user_owner(company, current_user)

        member = await self.members_repo.get_one_by(user_id=action.user_id, company_id=company.id)
        if not member:
            raise HTTPException(status_code=400, detail="no such member in the company")

        member_dict = member.model_dump()
        if member_dict["role"] != "admin":
            raise HTTPException(status_code=400, detail="member is not admin")
        member_dict["role"] = "member"
        await self.members_repo.update_one(member.id, member_dict)
        return True

    async def get_all_members(self, company_id: int, current_user: User):
        company = await self.company_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")

        await self.actions_permissions.is_user_owner(company, current_user)
        return await self.members_repo.get_all_by(company_id=company_id, role="member")

    async def get_all_admins(self, company_id: int, current_user: User):
        company = await self.company_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")

        await self.actions_permissions.is_user_owner(company, current_user)
        return await self.members_repo.get_all_by(company_id=company_id, role="admin")

    async def get_all_invitations(self, company_id: int, current_user: User):
        company = await self.company_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")

        await self.actions_permissions.is_user_owner(company, current_user)
        return await self.invitations_repo.get_all_by(company_id=company_id, is_accepted=None)

    async def get_all_requests(self, company_id: int, current_user: User):
        company = await self.company_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")

        await self.actions_permissions.is_user_owner(company, current_user)
        return await self.requests_repo.get_all_by(company_id=company_id, is_accepted=None)


class OwnerActionHandler:
    def __init__(self):
        self.action_service = OwnerActionsService(InvitationsRepository, RequestsRepository,
                                                  CompaniesRepository, UsersRepository, MembersRepository)

    async def handle_action(self, action: OwnerActionCreate, current_user: User):
        if action.action is OwnerActions.Send_invitation:
            return await self.action_service.send_invite(action, current_user)
        elif action.action is OwnerActions.Cancel_invitation:
            return await self.action_service.cancel_invite(action, current_user)
        elif action.action is OwnerActions.Accept_request:
            return await self.action_service.accept_request(action, current_user)
        elif action.action is OwnerActions.Deny_request:
            return await self.action_service.deny_request(action, current_user)
        elif action.action is OwnerActions.Delete_member:
            return await self.action_service.delete_member(action, current_user)
        elif action.action is OwnerActions.Add_admin:
            return await self.action_service.add_admin(action, current_user)
        elif action.action is OwnerActions.Remove_admin:
            return await self.action_service.remove_admin(action, current_user)

    async def get_all_invitations(self, company_id: int, current_user: User):
        return await self.action_service.get_all_invitations(company_id, current_user)

    async def get_all_requests(self, company_id: int, current_user: User):
        return await self.action_service.get_all_requests(company_id, current_user)

    async def get_all_members(self, company_id: int, current_user: User):
        return await self.action_service.get_all_members(company_id, current_user)

    async def get_all_admins(self, company_id: int, current_user: User):
        return await self.action_service.get_all_admins(company_id, current_user)
