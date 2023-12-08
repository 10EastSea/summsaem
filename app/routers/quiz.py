from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel) -> ResponseModel:
    try:
        content, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

        prompt = make_prompt(content, quiz_type, num_of_quiz)

        # TODO: (MAY) 두 로직 병렬 수행 가능 여부 확인
        summary = run_summary_with_clova_api(content) if is_summary else None
        quiz = run_prompt_with_openai_api(prompt)

        response = get_response_model(summary, quiz)
    except Exception:
        response = get_failure_response_model()
    
    return response
