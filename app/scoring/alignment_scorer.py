# app/scoring/alignment_scorer.py

import numpy as np

from app.nlp.embeddings import generate_embeddings_batch, cosine_similarity_matrix

# Sentences below this similarity threshold are considered non-matching.
# Prevents semantic noise from inflating scores (unrelated sentences still
# score ~0.3–0.45 with MiniLM, so we floor those out).
SIMILARITY_THRESHOLD = 0.45

def compute_alignment_score(
    cv_sentences: list[str], 
    jd_sentences: list[str],
    precision_weight: float = 0.4,
    recall_weight: float = 0.6,
) -> dict:
    if not cv_sentences or not jd_sentences:
        return _empty_result()

    # Batch encode everything in two forward passes (faster than for loops)
    cv_embeddings = generate_embeddings_batch(cv_sentences)
    jd_embeddings = generate_embeddings_batch(jd_sentences)
    
    # Similarity matrix: shape (n_cv, n_jd)
    similarity_matrix = cosine_similarity_matrix(cv_embeddings, jd_embeddings)
    
    # cv -> jd
    cv_best = np.max(similarity_matrix, axis=1)
    cv_matched = cv_best >= SIMILARITY_THRESHOLD
    precision = float(cv_best[cv_matched].mean()) if cv_matched.any() else 0.0

    # jd -> cv
    jd_best = np.max(similarity_matrix, axis=0)
    jd_matched = jd_best >= SIMILARITY_THRESHOLD
    recall = float(jd_best[jd_matched].mean()) if jd_matched.any() else 0.0

    assert abs(precision_weight + recall_weight - 1.0) < 1e-6, \
        "Weights must sum to 1.0"
    overall = precision_weight * precision + recall_weight * recall
    
    return {
        "overall_score": round(overall, 3),
        "precision":     round(precision, 3),   # relevance of CV to JD
        "recall":        round(recall, 3),       # JD coverage by CV
        "cv_sentences_matched": int(cv_matched.sum()),
        "cv_sentences_total":   len(cv_sentences),
        "jd_sentences_matched": int(jd_matched.sum()),
        "jd_sentences_total":   len(jd_sentences),
    }
    
def _empty_result() -> dict:
    return {
        "overall_score": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "cv_sentences_matched": 0,
        "cv_sentences_total": 0,
        "jd_sentences_matched": 0,
        "jd_sentences_total": 0,
    }
