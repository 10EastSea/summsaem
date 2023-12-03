from internal.model import RequestModel, ResponseModel

PROMPT_TEMPLATE = """
나는 내가 공부한 내용을 바탕으로 문제를 만들고 싶어.

문제는 유형은 {QUIZ_TYPE} 형식으로 만들어줘.
총 {NUM_OF_QUIZ}개의 문제를 만들어줘.
결과는 아래 양식처럼 JSON 형태로 만들어줘,
{
    1: {
        "question": "This is question 1.",
        "answer": "This is answer 1."
    },
    2: {
        "question": "This is question 2.",
        "answer": "This is answer 2."
    },
    ..
}
아래부터 끝까지는 내가 공부한 내용을 정리한 것이야.

{CONTENTS}
"""


def parse_request_model(request: RequestModel):
    return request.files, request.is_summary, request.quiz_type, request.num_of_quiz

def get_response_model(summary: str, quiz: dict()):
    return ResponseModel(summary=summary, quiz=quiz)


def make_contents(files: list):
    contents = "\n\n".join(files)
    print("[CONTENTS]:", contents)
    return contents
    
def make_prompt(contents: str, quiz_type: str, num_of_quiz: int):
    prompt = PROMPT_TEMPLATE.replace("{QUIZ_TYPE}", quiz_type)
    prompt = prompt.replace("{NUM_OF_QUIZ}", str(num_of_quiz))
    prompt = prompt.replace("{CONTENTS}", contents)
    print("[PROMPT]:", prompt)
    return prompt


def run_summary_with_clova_api(contents: str):
    """
    CLOVA Summary API를 이용해 summary를 만든다.
    - Reference: https://www.ncloud.com/product/aiService/clovaSummary
    """
    summary = "This is summary."
    return summary

def run_prompt_with_openai_api(prompt: str):
    """
    OpenAI API를 이용해 quiz를 만든다.
    - Reference: https://platform.openai.com/docs/introduction
    """
    quiz = {
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
    return quiz
