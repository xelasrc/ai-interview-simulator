# app/routes/interview.py

from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models.interview_models import InterviewRequest, InterviewResponse, SubmitAnswerRequest

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
def submit_answer_endpoint(session_id: str, request: SubmitAnswerRequest):
    updated_session = submit_answer(
        session_id, 
        request.answer_text, 
        request.timed_seconds
    )
    
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if len(updated_session.answers) == 0:
        raise HTTPException(status_code=400, detail="No answer recorded")

    latest_answer = updated_session.answers[-1]
    
    session_complete = (
        updated_session.current_index >= len(updated_session.questions)
    )
    
    return {
        "current_index": updated_session.current_index,
        "total_questions": len(updated_session.questions),
        "feedback": latest_answer.feedback,
        "session_complete": session_complete
    }

@router.get("/session/{session_id}")
def get_session_endpoint(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/session/{session_id}/summary")
def get_session_summary(session_id: str):
    session = get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if len(session.answers) == 0:
        raise HTTPException(status_code=400, detail="No answers recorded yet")

    total_questions = len(session.questions)
    total_answered = len(session.answers)

    scores = [
        answer.feedback.get("overall_score", 0)
        for answer in session.answers
        if answer.feedback
    ]

    average_score = sum(scores) / len(scores) if scores else 0

    best_answer = max(
        session.answers,
        key=lambda a: a.feedback.get("overall_score", 0) if a.feedback else 0
    )

    worst_answer = min(
        session.answers,
        key=lambda a: a.feedback.get("overall_score", 0) if a.feedback else 0
    )

    return {
        "total_questions": total_questions,
        "total_answered": total_answered,
        "average_score": round(average_score, 2),
        "best_question": best_answer.question,
        "best_score": best_answer.feedback.get("overall_score", 0),
        "weakest_question": worst_answer.question,
        "weakest_score": worst_answer.feedback.get("overall_score", 0),
    }