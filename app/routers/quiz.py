from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel):
    files, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

    contents = make_contents(files)
    prompt = make_prompt(contents, quiz_type, num_of_quiz)

    summary = run_summary_with_clova_api(contents) if is_summary else None
    quiz = run_prompt_with_openai_api(prompt)

    response = get_response_model(summary, quiz)
    return response
