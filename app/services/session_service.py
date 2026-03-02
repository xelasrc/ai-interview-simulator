# app/services/session_question.py

from typing import Dict

from app.models.session_models import InterviewSession, Answer
from app.scoring.answer_scorer import score_answer

# Simple in-memory store for MVP, will update later to Redis or a db for persistence
sessions: Dict[str, InterviewSession] = {}

def create_session(questions, timed=False):
    session = InterviewSession(questions=questions, timed=timed)
    sessions[str(session.session_id)] = session
    return session

def get_session(session_id: str):
    return sessions.get(session_id)

def submit_answer(session_id: str, answer_text: str, timed_seconds: int = None):
    session = sessions.get(session_id)
    
    if not session:
        return None
    
    if session.current_index >= len(session.questions):
        return None
    
    question = session.questions[session.current_index]
    
    feedback = score_answer(question, answer_text)
    
    session.answers.append(
        Answer(
            question=question, 
            answer_text=answer_text, 
            timed_seconds=timed_seconds,
            feedback=feedback
        )
    )
    
    session.current_index += 1
    return session