# app/routes/interview.py

from fastapi import APIRouter
from uuid import uuid4

from app.models.interview_models import InterviewRequest, InterviewResponse
from app.services.document_parser import DocumentParser
from app.scoring.alignment_scorer import compute_alignment_score
from app.services.question_service import generate_questions

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

@router.post("/alignment-score")
def alignment_score(request: InterviewRequest):
    cv_parser = DocumentParser(request.cv_text)
    jd_parser = DocumentParser(request.job_description)

    cv_sentences = cv_parser.extract_sentences()
    jd_sentences = jd_parser.extract_sentences()

    score = compute_alignment_score(cv_sentences, jd_sentences)

    return {
        "alignment_score": score
    }
    
@router.post("/generate-questions")
def generate_interview_questions(request: InterviewRequest):
    questions = generate_questions(
        request.cv_text,
        request.job_description,
        request.num_questions
    )

    return {
        "questions": questions,
        "timed": request.timed
    }