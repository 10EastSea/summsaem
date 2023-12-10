import json
from openai import OpenAI
from internal.model import RequestModel, ResponseModel
from internal.maintenance import *
from internal.variables import *


def parse_request_model(request: RequestModel):
    return request.content, request.summaryRequired, request.questionType, request.numberOfQuestions

def get_response_model(summary: str, quiz: list):
    return ResponseModel(success=True, summary=summary, questions=quiz, message=SUCCESS_MESSAGE_TEPLATE)


async def get_summary(summary_prompt: str):
    if summary_prompt is None:
        return None
    return await run_summary_prompt_with_openai_api(summary_prompt)

async def get_quiz(quiz_prompt: str):
    return await run_quiz_prompt_with_openai_api(quiz_prompt)


def make_summary_prompt(is_summary: bool, content: str):
    if not is_summary:
        return None
    
    summary_prompt = SUMMARY_PROMPT_TEMPLATE.replace("{CONTENT}", content)
    summary_prompt = summary_prompt[:LIMIT_OPENAI_API_CHARACTER]
    return summary_prompt

def make_quiz_prompt(content: str, quiz_type: str, num_of_quiz: int):
    # TODO: (MAY) prompt 제작 고도화
    quiz_prompt = QUIZ_PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", QUIZ_TYPE_LIST[quiz_type]) \
                                      .replace("{NUM_OF_QUIZ}", str(num_of_quiz)) \
                                      .replace("{CONTENT}", content)
    quiz_prompt = quiz_prompt[:LIMIT_OPENAI_API_CHARACTER]
    return quiz_prompt


async def run_summary_prompt_with_openai_api(summary_prompt: str):
    print_log("INPUT", "summary prompt", summary_prompt)
    result = await _run_prompt_with_openai_api(summary_prompt)
    print_log("OUTPUT", "summary result", result)

    summary = result
    return summary

async def run_quiz_prompt_with_openai_api(quiz_prompt: str):
    print_log("INPUT", "quiz prompt", quiz_prompt)
    result = await _run_prompt_with_openai_api(quiz_prompt)
    print_log("OUTPUT", "quiz result", result)

    # TODO: (MAY - High importance) 원하는대로 API 결과 만들어지지 않을 경우 -> 파싱 로직 구현
    quiz = json.loads(result)
    quiz = [v for _, v in quiz.items()]
    return quiz


async def _run_prompt_with_openai_api(prompt: str):
    """
    OpenAI API를 이용해 quiz를 만든다.
    - Reference: https://platform.openai.com/docs/introduction
    - API docs: https://platform.openai.com/docs/overview
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model=GPT_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_ROLE_CONTENT},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content
    return result
