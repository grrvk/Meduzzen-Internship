from fastapi import APIRouter, Depends, Query
from typing import Annotated
from starlette import status
from app.auth.utils_auth import check_token
from app.schemas.answers import AnswerCreateRequest, AnswerUpdateRequest
from app.schemas.questions import QuestionCreateRequest, QuestionUpdateRequest
from app.schemas.quizzes import QuizCreateRequest, QuizUpdateRequest
from app.schemas.response import Response
from app.schemas.user_answer import UserAnswerSchema, UserAnswerListSchema
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, quizzes_service, results_service
from app.services.quizzes import QuizzesService
from app.services.results import ResultsService

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


@router.delete("/quizzes/{quiz_id}", response_model=Response[bool])
async def delete_quiz(
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


@router.put("/quizzes/{quiz_id}", response_model=Response[bool])
async def update_quiz(
        quiz_id: int,
        quiz: QuizUpdateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.edit_quiz(quiz_id, quiz, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="updated",
        result=res
    )


@router.post("/quizzes/{quiz_id}", response_model=Response[int])
async def add_question(
        quiz_id: int,
        question: QuestionCreateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.add_question(quiz_id, question, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="added",
        result=res
    )


@router.put("/quizzes/{quiz_id}/{question_id}", response_model=Response[bool])
async def update_question(
        quiz_id: int,
        question_id: int,
        question: QuestionUpdateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.edit_question(quiz_id, question_id, question, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="updated",
        result=res
    )


@router.delete("/quizzes/{quiz_id}/{question_id}", response_model=Response[bool])
async def delete_question(
        quiz_id: int,
        question_id: int,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.delete_question(quiz_id, question_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="deleted",
        result=res
    )


@router.post("/quizzes/{quiz_id}/{question_id}", response_model=Response[int])
async def add_answer(
        quiz_id: int,
        question_id: int,
        answer: AnswerCreateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.add_answer(quiz_id, question_id, answer, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="added",
        result=res
    )


@router.put("/quizzes/{quiz_id}/{question_id}/{answer_id}", response_model=Response[bool])
async def update_answer(
        quiz_id: int,
        question_id: int,
        answer_id: int,
        answer: AnswerUpdateRequest,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.edit_answer(quiz_id, question_id, answer_id, answer, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="updated",
        result=res
    )


@router.delete("/quizzes/{quiz_id}/{question_id}/{answer_id}", response_model=Response[bool])
async def delete_answer(
        quiz_id: int,
        question_id: int,
        answer_id: int,
        quiz_service: Annotated[QuizzesService, Depends(quizzes_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await quiz_service.delete_answer(quiz_id, question_id, answer_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="deleted",
        result=res
    )



