import asyncio
from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel) -> ResponseModel:
    try:
        content, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

        prompt = make_prompt(content, quiz_type, num_of_quiz)

        get_summary_task = asyncio.create_task(get_summary(is_summary, content))
        get_quiz_task = asyncio.create_task(get_quiz(prompt))
        summary, quiz = await asyncio.gather(get_summary_task, get_quiz_task)

        response = get_response_model(summary, quiz)
    except Exception:
        response = get_failure_response_model()
    
    return response
