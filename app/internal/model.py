from fastapi import UploadFile
from pydantic import BaseModel
from typing import Dict, List

QUIZ_TYPE_LIST = [
    "ox형",
    "객관형",
    "약술형",
    "서술형",
    "논술형",
    "면접",
    "설문지"
]


class QuizItem(BaseModel):
    question: str
    answer: str


class RequestModel(BaseModel):
    file: List[str]  # List[UploadFile]
    questionType: int
    numberOfQuestions: int
    summaryRequired: bool

class ResponseModel(BaseModel):
    summary: str | None
    quiz: Dict[int, QuizItem]
