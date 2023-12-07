import json
import os
import requests
from openai import OpenAI
from internal.model import RequestModel, ResponseModel

CLOVA_SUMMARY_API = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"

PROMPT_TEMPLATE = """
나는 내가 공부한 내용을 바탕으로 문제를 만들고 싶어.

문제는 유형은 {QUIZ_TYPE} 형식으로 만들어줘.
총 {NUM_OF_QUIZ}개의 문제를 만들어줘.
결과는 아래 양식처럼 JSON 형태로 만들어줘,
{
    "1": {
        "question": "This is question 1.",
        "answer": "This is answer 1."
    },
    "2": {
        "question": "This is question 2.",
        "answer": "This is answer 2."
    },
    ..
}
아래부터 끝까지는 내가 공부한 내용을 정리한 것이야.

{CONTENT}
"""

QUIZ_TYPE_LIST = [
    "ox형", "객관형", "약술형", "서술형", "논술형", "면접", "설문지"
]


def parse_request_model(request: RequestModel):
    print("[INPUT:CONTENT]:", request.content, "\n")
    return request.content, request.summaryRequired, request.questionType, request.numberOfQuestions

def get_response_model(summary: str, quiz: dict()):
    return ResponseModel(success=True, summary=summary, questions=quiz, message="Questions created successfully")

    
def make_prompt(content: str, quiz_type: str, num_of_quiz: int):
    # TODO: (MAY) prompt 제작 고도화
    prompt = PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", QUIZ_TYPE_LIST[quiz_type])
    prompt = prompt.replace("{NUM_OF_QUIZ}", str(num_of_quiz))
    prompt = prompt.replace("{CONTENT}", content)
    print("[INPUT:PROMPT]:", prompt)
    return prompt


def run_summary_with_clova_api(content: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    - API docs: https://api.ncloud-docs.com/docs/ai-naver-clovasummary-api
    """
    # TODO: 글자 제한 2000자 -> 개선할 수 있는 방법은? (여러번 호출?)
    content = content[:1000]

    # TODO: API Call 에러 처리
    # TODO: content 길에 맞게 요약 생성 문장 결정
    # TODO: (MAY) 적절한 제목 생성 로직 추가
    headers = {
        "X-NCP-APIGW-API-KEY-ID": os.getenv("NCP_APIGW_API_KEY_ID"),
        "X-NCP-APIGW-API-KEY": os.getenv("NCP_APIGW_API_KEY"),
        "Content-Type": "application/json"
    }
    data = {
        "document": {
            "title": content[:content.find("\n")],
            "content": content
        },
        "option": {
            "language": "ko",
            "model": "general",
            "tone": 0,
            "summaryCount": 5
        }
    }
    print("[INPUT:CONTENT DATA]:", data)

    response = requests.post(url=CLOVA_SUMMARY_API, headers=headers, json=data)
    print("[OUPUT:SUMMARY RESULT (RAW)]", response.text)

    summary = json.loads(response.text)["summary"]
    print("[OUTPUT:SUMMARY]:", summary)
    return summary

def run_prompt_with_openai_api(prompt: str):
    """
    OpenAI API를 이용해 quiz를 만든다.
    - Reference: https://platform.openai.com/docs/introduction
    - API docs: https://platform.openai.com/docs/overview
    """
    # TODO: (MAY) 생성형 AI 답변 튜닝 포인트 발견 후 개선
    # TODO: (MAY) 오래 걸리는 응답 개선 포인트 찾기
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content
    print("[OUTPUT:QUIZ RESULT (RAW)]:", result)

    # TODO: (MAY - High importance) 원하는대로 API 결과 만들어지지 않을 경우 -> 파싱 로직 구현
    quiz = json.loads(result)
    quiz = [v for _, v in quiz.items()]
    print("[OUTPUT:QUIZ]:", quiz)
    return quiz

# TODO:
# 1. API Call 및 예기치 못한 응답 에러 처리
# 2. print 문 공통화
