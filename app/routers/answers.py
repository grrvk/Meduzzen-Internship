from fastapi import APIRouter, Depends
from typing import Annotated

from redis import Redis
from starlette import status
from app.auth.utils_auth import check_token
from app.db.database import get_redis_db
from app.schemas.response import Response
from app.schemas.user_answer_redis import AnswerDataDetail, AnswerData
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, results_service
from app.services.results import ResultsService

router = APIRouter(tags=["answers"])


@router.get("/answers", response_model=list[AnswerDataDetail])
async def get_answers(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        redis_client: Annotated[Redis, Depends(get_redis_db)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_results(current_user, redis_client)


@router.get("/answers/users/{user_id}", response_model=list[AnswerDataDetail])
async def get_answers_for_user(
        user_id: int,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        redis_client: Annotated[Redis, Depends(get_redis_db)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_results_for_user(current_user, user_id, redis_client)


@router.get("/answers/companies/{company_id}", response_model=list[AnswerData])
async def get_answers_for_company(
        company_id: int,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        redis_client: Annotated[Redis, Depends(get_redis_db)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await result_service.get_all_results_for_company(current_user, company_id, redis_client)


