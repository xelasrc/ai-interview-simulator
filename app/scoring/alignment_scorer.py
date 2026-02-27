# app/scoring/alignment_scorer.py

from app.nlp.embeddings import generate_embedding, cosine_similarity

def compute_alignment_score(cv_sentences, jd_sentences):
    if not cv_sentences or not jd_sentences:
        return 0.0

    scores = []

    for cv_sentence in cv_sentences:
        cv_embedding = generate_embedding(cv_sentence)

        sentence_scores = []
        for jd_sentence in jd_sentences:
            jd_embedding = generate_embedding(jd_sentence)
            similarity = cosine_similarity(cv_embedding, jd_embedding)
            sentence_scores.append(similarity)

        scores.append(max(sentence_scores))

    return float(round(sum(scores) / len(scores), 3))