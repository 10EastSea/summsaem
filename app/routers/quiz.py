from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel):
    content, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

    prompt = make_prompt(content, quiz_type, num_of_quiz)

    summary = run_summary_with_clova_api(content) if is_summary else None
    quiz = run_prompt_with_openai_api(prompt)

    response = get_response_model(summary, quiz)
    return response
