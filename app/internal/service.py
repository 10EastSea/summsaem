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


async def get_summary(is_summary: bool, content: str):
    if not is_summary:
        return None
    return await run_summary_with_clova_api(content)

async def get_quiz(prompt: str):
    return await run_prompt_with_openai_api(prompt)

    
def make_prompt(content: str, quiz_type: str, num_of_quiz: int):
    # TODO: (MAY) prompt 제작 고도화
    prompt = PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", QUIZ_TYPE_LIST[quiz_type]) \
                            .replace("{NUM_OF_QUIZ}", str(num_of_quiz)) \
                            .replace("{CONTENT}", content)
    
    print_log("INPUT", "prompt", prompt)
    return prompt


async def run_summary_with_clova_api(content: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    - API docs: https://api.ncloud-docs.com/docs/ai-naver-clovasummary-api
    """
    # TODO: 글자 제한 2000자 -> 개선할 수 있는 방법은? (여러번 호출?)
    content = content[:1964]

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
    # TODO: (MAY) 생성형 AI 답변 튜닝 포인트 발견 후 개선
    client = OpenAI()
    completion = client.chat.completions.create(
        model=GPT_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content
    print_log("OUTPUT", "quiz result", result)

    # TODO: (MAY - High importance) 원하는대로 API 결과 만들어지지 않을 경우 -> 파싱 로직 구현
    quiz = json.loads(result)
    quiz = [v for _, v in quiz.items()]
    return quiz
