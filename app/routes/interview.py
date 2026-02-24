# app/routes/interview.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class InterviewRequest(BaseModel):
    job_description: str
    cv_text: str
    num_questions: int
    timed: bool

@router.post("/generate")
def generate_interview(request: InterviewRequest):
    return{
        "message": "Interview session created",
        "num_questions": request.num_questions,
        "timed": request.timed
    }