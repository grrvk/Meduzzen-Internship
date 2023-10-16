from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from app.auth.utils_auth import check_token
from app.schemas.answers import AnswerCreateRequest
from app.schemas.questions import QuestionCreateRequest
from app.schemas.quizzes import QuizCreateRequest
from app.schemas.response import Response
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, quizzes_service
from app.services.quizzes import QuizzesService

router = APIRouter(tags=["quizzes"])


@router.post("/quizzes", response_model=Response[int])
async def add_quiz(
        quiz: QuizCreateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.add_quiz(quiz, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="added",
        result=res
    )


@router.delete("/quizzes/{quiz_id}", response_model=Response[int])
async def add_quiz(
        quiz_id: int,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.delete_quiz(quiz_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="deleted",
        result=res
    )


@router.get("/companies/{company_id}/quizzes", response_model=Response[int])
async def add_quiz(
        company_id: int,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.get_all_quizzes(company_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )