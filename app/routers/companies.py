from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from app.auth.utils_auth import check_token
from app.schemas.companies import CompanyCreateRequest, CompanyUpdateRequest, CompaniesListResponse, CompanySchema
from app.schemas.quizzes import QuizDetailsSchema
from app.schemas.response import Response
from app.services.auth import AuthService
from app.services.companies import CompaniesService
from app.services.dependencies import authentication_service, companies_service, quizzes_service
from app.services.quizzes import QuizzesService

router = APIRouter(tags=["companies"])


@router.post("/add_company", response_model=Response[int])
async def add_company(
        company: CompanyCreateRequest,
        company_service: Annotated[CompaniesService, Depends(companies_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await company_service.add_company(company, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="added",
        result=res
    )


@router.put("/companies/{company_id}", response_model=Response[int])
async def update_company(
        company_id: int,
        company: CompanyUpdateRequest,
        company_service: Annotated[CompaniesService, Depends(companies_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await company_service.edit_company(company_id, company, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="updated",
        result=res
    )


@router.delete("/companies/{company_id}", response_model=Response[int])
async def delete_company(
        company_id: int,
        company_service: Annotated[CompaniesService, Depends(companies_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await company_service.delete_company(company_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.get("/companies", response_model=list[CompaniesListResponse])
async def get_all_companies(
        company_service: Annotated[CompaniesService, Depends(companies_service)]
):
    return await company_service.get_all_companies()


@router.get("/companies/{company_id}", response_model=Response[CompanySchema])
async def read_item(
        company_id: int,
        company_service: Annotated[CompaniesService, Depends(companies_service)]
):
    res = await company_service.get_company_by_id(company_id)
    return Response(
            status_code=status.HTTP_200_OK,
            detail="OK",
            result=res
        )


@router.get("/companies/{company_id}/quizzes", response_model=list[QuizDetailsSchema])
async def add_quiz(
        company_id: int,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await quiz_service.get_all_quizzes(company_id, current_user)

