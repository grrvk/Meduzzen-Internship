from fastapi import APIRouter, Depends
from typing import Annotated

from redis import Redis
from starlette import status
from app.auth.utils_auth import check_token
from app.db.database import get_redis_db
from app.schemas.response import Response
from app.schemas.user_answer import UserAnswerListSchema
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, results_service
from app.services.results import ResultsService

router = APIRouter(tags=["results"])


@router.post("/results/{quiz_id}", response_model=Response[int])
async def pass_quiz(
        quiz_id: int,
        company_id: int,
        user_answers: UserAnswerListSchema,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        redis_client: Annotated[Redis, Depends(get_redis_db)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await result_service.get_result(company_id, quiz_id, user_answers, current_user, redis_client)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="passed",
        result=res
    )


@router.get("/results", response_model=Response[int])
async def get_average_total(
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


@router.get("/results/{company_id}", response_model=Response[int])
async def get_company_rating(
        company_id: int,
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await result_service.get_average_in_company(company_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.get("/csv", response_model=Response[bool])
async def get_results_csv(
        result_service: Annotated[ResultsService, Depends(results_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        redis_client: Annotated[Redis, Depends(get_redis_db)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await result_service.export_to_csv(redis_client, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )



