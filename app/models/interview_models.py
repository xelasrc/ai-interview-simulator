from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class InterviewRequest(BaseModel):
    job_description: str
    cv_text: str
    num_questions: int
    timed: bool

class InterviewResponse(BaseModel):
    session_id: UUID
    num_questions: int
    timed: bool
class SubmitAnswerRequest(BaseModel):
    answer_text: Optional[str] = None
    timed_seconds: Optional[int] = None