# app/routes/interview.py

from fastapi import APIRouter
from uuid import uuid4

from app.models.interview_models import InterviewRequest, InterviewResponse

router = APIRouter()

@router.post("/generate", response_model=InterviewResponse)
def generate_interview(request: InterviewRequest):
    session_id = uuid4()

    return InterviewResponse(
        session_id=session_id,
        num_questions=request.num_questions,
        timed=request.timed
    )