import json
import os
import requests
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
    # return await run_summary_with_clova_api(summary_prompt)
    return await run_summary_prompt_with_openai_api(summary_prompt)

async def get_quiz(quiz_prompt: str):
    return await run_quiz_prompt_with_openai_api(quiz_prompt)


def make_summary_prompt(is_summary: bool, content: str):
    if not is_summary:
        return None
    
    summary_prompt = SUMMARY_PROMPT_TEMPLATE.replace("{CONTENT}", content)
    summary_prompt = summary_prompt[:LIMIT_OPENAI_API_CHARACTER]

    print_log("INPUT", "summary_prompt", summary_prompt)
    # return content
    return summary_prompt

def make_quiz_prompt(content: str, quiz_type: str, num_of_quiz: int):
    # TODO: (MAY) prompt 제작 고도화
    quiz_prompt = QUIZ_PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", QUIZ_TYPE_LIST[quiz_type]) \
                                      .replace("{NUM_OF_QUIZ}", str(num_of_quiz)) \
                                      .replace("{CONTENT}", content)
    quiz_prompt = quiz_prompt[:LIMIT_OPENAI_API_CHARACTER]

    print_log("INPUT", "quiz_prompt", quiz_prompt)
    return quiz_prompt


async def run_summary_with_clova_api(content: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    - API docs: https://api.ncloud-docs.com/docs/ai-naver-clovasummary-api
    """
    # TODO: 글자 제한 2000자 -> 개선할 수 있는 방법은? (여러번 호출?)
    content = content[:LIMIT_CLOVA_SUMMARY_API_CHARACTER]

    # TODO: content 길이에 맞게 summaryCount 결정
    headers = {
        "X-NCP-APIGW-API-KEY-ID": os.getenv("NCP_APIGW_API_KEY_ID"),
        "X-NCP-APIGW-API-KEY": os.getenv("NCP_APIGW_API_KEY"),
        "Content-Type": "application/json"
    }
    data = {
        "document": {
            "content": content
        },
        "option": {
            "language": "ko",
            "model": "general",
            "tone": 0,
            "summaryCount": 5
        }
    }
    print_log("INPUT", "summary request.data", data)

    response = requests.post(url=CLOVA_SUMMARY_API, headers=headers, json=data)
    print_log("OUTPUT", "summary response.text", response.text)

    summary = json.loads(response.text)["summary"]
    return summary

async def run_prompt_with_openai_api(prompt: str):
    """
    OpenAI API를 이용해 quiz를 만든다.
    - Reference: https://platform.openai.com/docs/introduction
    - API docs: https://platform.openai.com/docs/overview
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model=GPT_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content
    return result

async def run_summary_prompt_with_openai_api(summary_prompt: str):
    result = await run_prompt_with_openai_api(summary_prompt)
    print_log("OUTPUT", "summary result", result)

    summary = result
    return summary

async def run_quiz_prompt_with_openai_api(quiz_prompt: str):
    result = await run_prompt_with_openai_api(quiz_prompt)
    print_log("OUTPUT", "quiz result", result)

    # TODO: (MAY - High importance) 원하는대로 API 결과 만들어지지 않을 경우 -> 파싱 로직 구현
    quiz = json.loads(result)
    quiz = [v for _, v in quiz.items()]
    return quiz
