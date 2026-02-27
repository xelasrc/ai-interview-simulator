# app/routes/interview.py

from fastapi import APIRouter
from uuid import uuid4

from app.models.interview_models import InterviewRequest, InterviewResponse

from app.services.document_parser import DocumentParser

router = APIRouter()

@router.post("/generate", response_model=InterviewResponse)
def generate_interview(request: InterviewRequest):
    session_id = uuid4()

    return InterviewResponse(
        session_id=session_id,
        num_questions=request.num_questions,
        timed=request.timed
    )
    
@router.post("/parse-test")
def parse_test(request: InterviewRequest):
    cv_parser = DocumentParser(request.cv_text)
    jd_parser = DocumentParser(request.job_description)

    return {
        "cv_sentences": cv_parser.extract_sentences(),
        "cv_keywords": cv_parser.extract_keywords(),
        "jd_sentences": jd_parser.extract_sentences(),
        "jd_keywords": jd_parser.extract_keywords(),
    }