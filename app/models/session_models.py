# app/models/session_models.py

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4

class Answer(BaseModel):
    question: str
    answer_text: Optional[str] = None
    timed_seconds: Optional[int] = None
    feedback: Optional[dict] = None
    
class InterviewSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    questions: List[str]
    answers: List[Answer] = Field(default_factory=list)
    current_index: int = 0
    timed: bool = False