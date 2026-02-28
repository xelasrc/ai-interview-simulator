# app/models/session_models.py

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

class Answer(BaseModel):
    question: str
    answer_text: Optional[str]
    timed_seconds: Optional[int]
    
class InterviewSession(BaseModel):
    session_id: UUID = uuid4()
    questions: List[str]
    answers: List[str] = []
    current_index: int = 0
    timed: bool = False