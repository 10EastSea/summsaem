GPT_MODEL_NAME = "gpt-3.5-turbo"
SYSTEM_ROLE_CONTENT = "You are a helpful assistant."

ONE_CHARACTER_BUFFER = 8
LIMIT_OPENAI_API_CHARACTER = 4096 - ONE_CHARACTER_BUFFER

QUIZ_TYPE_LIST = [
    "ox형", "객관형", "약술형", "서술형", "논술형", "면접", "설문지"
]

SUCCESS_MESSAGE_TEPLATE = "Questions created successfully"
FAIL_MESSAGE_TEPLATE = "Question creation failed: {REASON}"

LOG_TEMPLATE = """
[{DATE_TIME}] {IO_TYPE} - {TARGET_NAME}
{CONTENT}
"""

SUMMARY_PROMPT_TEMPLATE = """아래는 내가 공부한 내용이야. 해당 내용을 요약해줘.

{CONTENT}"""

QUIZ_PROMPT_TEMPLATE = """나는 내가 공부한 내용을 바탕으로 문제를 만들고 싶어.

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

{CONTENT}"""
