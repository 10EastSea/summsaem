from pydantic import BaseModel
from typing import List


class QuizItem(BaseModel):
    question: str
    answer: str

class RequestModel(BaseModel):
    content: str
    questionType: int
    numberOfQuestions: int
    summaryRequired: bool

class ResponseModel(BaseModel):
    success: bool
    summary: str | None
    questions: List[QuizItem] | None
    message: str
