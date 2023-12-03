from pydantic import BaseModel
from typing import Dict, List


class QuizItem(BaseModel):
    question: str
    answer: str


class RequestModel(BaseModel):
    files: List[str]
    is_summary: bool
    quiz_type: str
    num_of_quiz: int

class ResponseModel(BaseModel):
    summary: str | None
    quiz: Dict[int, QuizItem]
