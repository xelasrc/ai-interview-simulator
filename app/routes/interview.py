# app/routes/interview.py

from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models.interview_models import InterviewRequest, InterviewResponse
from app.models.session_models import Answer

from app.services.document_parser import DocumentParser
from app.services.question_service import generate_questions
from app.services.session_service import create_session, get_session, submit_answer

from app.scoring.alignment_scorer import compute_alignment_score

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

@router.post("/start-session")
def start_session(request: InterviewRequest):
    questions = generate_questions(
        request.cv_text, 
        request.job_description, 
        request.num_questions
    )
    session = create_session(questions, timed=request.timed)
    return {
        "session_id": str(session.session_id), 
        "questions": questions if not request.timed else None
    }

@router.post("/submit-answer/{session_id}")
def submit_answer_endpoint(session_id: str, answer: Answer):
    updated_session = submit_answer(session_id, answer.answer_text, answer.timed_seconds)
    
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found or already complete")
    
    latest_answer = updated_session.answers[-1]

    return {
        "current_index": updated_session.current_index, 
        "total_questions": len(updated_session.questions),
        "feedback": latest_answer.feedback 
    }

@router.get("/session/{session_id}")
def get_session_endpoint(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session