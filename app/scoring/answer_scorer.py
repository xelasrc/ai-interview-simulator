# app/scoring/answer_scorer.py

from app.nlp.embeddings import generate_embedding, cosine_similarity

def score_answer(question: str, answer: str):
    # Relevance (semantic similarity)
    question_embedding = generate_embedding(question)
    answer_embedding = generate_embedding(answer)
    
    relevance_score = cosine_similarity(question_embedding, answer_embedding)
    
    # Length score
    word_count = len(answer.split())
    length_score = min(word_count / 150, 1.0) #150 words = full score
    
    # Basic STAR detection
    star_keywords = ["situation", "task", "action", "result"]
    star_hits = sum(1 for word in star_keywords if word in answer.lower())
    star_score = star_hits / 4

    # Normalize relevance to 0–1 if needed
    relevance_score = float(max(0, min(relevance_score, 1)))

    overall_score = (
        0.5 * relevance_score +
        0.3 * length_score +
        0.2 * star_score
    )
    
    return {
        "relevance_score": round(relevance_score, 2),
        "length_score": round(length_score, 2),
        "star_score": round(star_score, 2),
        "overall_score": round(overall_score, 2),
        "word_count": word_count
    }