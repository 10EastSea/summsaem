from fastapi import APIRouter
from internal.model import RequestModel, ResponseModel
from internal.service import *

quiz = APIRouter(prefix="/quiz")


@quiz.post("/create")
async def create_quiz(request: RequestModel):
    """
    Request:
    {
        "files": ["This is file 1 content.", "This is file 2 content.", "This is file 3 content."],
        "is_summary": true,
        "quiz_type": "QUIZ_TYPE",
        "num_of_quiz": 10
    }

    Response:
    {
        "summary": "This is summary.",
        "quiz": {
            1: {
                "question": "This is question 1.",
                "answer": "This is answer 1."
            },
            2: {
                "question": "This is question 2.",
                "answer": "This is answer 2."
            },
            3: {
                "question": "This is question 3.",
                "answer": "This is answer 3."
            }
        }
    }
    """
    files, is_summary, quiz_type, num_of_quiz = parse_request_model(request)

    contents = make_contents(files)
    prompt = make_prompt(contents, quiz_type, num_of_quiz)

    summary = run_summary_with_clova_api(contents) if is_summary else None
    quiz = run_prompt_with_openai_api(prompt)

    response = get_response_model(summary, quiz)
    return response
