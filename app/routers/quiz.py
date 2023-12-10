import asyncio
from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel) -> ResponseModel:
    try:
        content, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

        summary_prompt = make_summary_prompt(is_summary, content)
        quiz_prompt = make_quiz_prompt(content, quiz_type, num_of_quiz)

        get_summary_task = asyncio.create_task(get_summary(summary_prompt))
        get_quiz_task = asyncio.create_task(get_quiz(quiz_prompt))
        summary, quiz = await asyncio.gather(get_summary_task, get_quiz_task)

        response = get_response_model(summary, quiz)
    except Exception:
        response = get_failure_response_model()
    
    return response
