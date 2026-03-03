# app/scoring/alignment_scorer.py

import numpy as np

from app.nlp.embeddings import generate_embeddings_batch, cosine_similarity_matrix

def compute_alignment_score(cv_sentences, jd_sentences):
    if not cv_sentences or not jd_sentences:
        return {
        "cv_to_jd_score": 0,
        "jd_to_cv_score": 0,
        "overall_score": 0
    }

    cv_embeddings = generate_embeddings_batch(cv_sentences)
    jd_embeddings = generate_embeddings_batch(jd_sentences)
    
    similarity_matrix = cosine_similarity_matrix(cv_embeddings, jd_embeddings)
    
    # cv -> jd
    cv_best = np.max(similarity_matrix, axis=1)
    cv_to_jd = float(round(np.mean(cv_best), 3))
    
    # jd -> cv
    jd_best = np.max(similarity_matrix, axis=0)
    jd_to_cv = float(round(np.mean(jd_best), 3))
    
    overall = float(round((cv_to_jd + jd_to_cv) / 2, 3))
    
    return {
        "cv_to_jd": cv_to_jd,
        "jd_to_cv": jd_to_cv,
        "overall": overall
    }