import json
from fastapi import UploadFile
from openai import OpenAI
from internal.model import QUIZ_TYPE_LIST
from internal.model import RequestModel, ResponseModel

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

{CONTENTS}
"""


def parse_request_model(request: RequestModel):
    # TODO: 파일 받기 가능 여부 확인
    
    return request.file, request.summaryRequired, request.questionType, request.numberOfQuestions

def get_response_model(summary: str, quiz: dict()):
    return ResponseModel(summary=summary, quiz=quiz)


def make_contents(files: list):
    contents = "\n\n".join(files)
    print("[CONTENTS]:", contents)
    return contents
    
def make_prompt(contents: str, quiz_type: str, num_of_quiz: int):
    prompt = PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", QUIZ_TYPE_LIST[quiz_type])
    prompt = prompt.replace("{NUM_OF_QUIZ}", str(num_of_quiz))
    prompt = prompt.replace("{CONTENTS}", contents)
    print("[PROMPT]:", prompt)
    return prompt


def run_summary_with_clova_api(contents: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    """
    # TODO: CLOVA API 연동 필요

    summary = "This is summary."
    return summary

def run_prompt_with_openai_api(prompt: str):
    """
    OpenAI API를 이용해 quiz를 만든다.
    - Reference: https://platform.openai.com/docs/introduction
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content
    print("[RESULT]:", result)

    # TODO: 파싱 로직 구현 필요
    quiz = json.loads(result)
    return quiz
