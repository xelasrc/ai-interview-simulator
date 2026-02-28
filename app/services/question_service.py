# app/services/question_service.py

from openai import OpenAI
import os

def generate_questions(cv_text, job_description, num_questions):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f""" 
    You are an expert technical interviewer.
    Based on the following CV and job description, generate {num_questions} interview questions.
    
    Focus on:
    - Technical depth 
    - Behavioural competency
    - Real-world experience

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Return only the list of questions.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    text_output = response.choices[0].message.content

    # Simple split for MVP
    questions = [q.strip("- ").strip() for q in text_output.split("\n") if q.strip()]

    
    return questions[:num_questions]