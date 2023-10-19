from fastapi import APIRouter, Depends
from typing import Annotated

from redis import Redis
from starlette import status
from app.auth.utils_auth import check_token
from app.db.database import get_redis_db
from app.schemas.quizzes import QuizDateRequest
from app.schemas.response import Response
from app.schemas.result import AverageResultListDetail, CompanyAverageResultForUserListDetail, \
    UserAverageResultDateListDetail, UserPassingDateListDetail
from app.schemas.user_answer import UserAnswerListSchema
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, results_service
from app.services.results import ResultsService

router = APIRouter(tags=["analytics"])


@router.get("/analytics/average", response_model=Response[int])
async def analytics_average_total(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await result_service.get_average_total(current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.get("/analytics/my_average", response_model=list[AverageResultListDetail])
async def get_my_average_results_list(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_average_results_list(current_user)


@router.get("/analytics/quizzes", response_model=list[QuizDateRequest])
async def get_quizzes_dates_list(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_quizzes_dates_list(current_user)


@router.get("/analytics/members_average", response_model=list[CompanyAverageResultForUserListDetail])
async def get_members_average_results_list(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_all_members_averages(current_user)


@router.get("/analytics/{user_id}", response_model=list[UserAverageResultDateListDetail])
async def get_member_averages(
        user_id: int,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_member_averages(user_id, current_user)


@router.get("/analytics/dates/{company_id}", response_model=list[UserPassingDateListDetail])
async def get_company_members_passing_dates(
        company_id: int,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_company_members_passing_dates(company_id, current_user)
