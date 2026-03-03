# app/nlp/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def generate_embedding(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)

def generate_embeddings_batch(texts: list[str]) -> np.ndarray:
    """
    Encode a list of texts in a single forward pass.
    Much faster than calling generate_embedding() in a loop.
    """
    return model.encode(texts, convert_to_numpy=True, batch_size=64, show_progress_bar=False)
    
def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return float(np.dot(vec1, vec2) / denom) if denom else 0.0

def cosine_similarity_matrix(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
    """
    Compute pairwise cosine similarities between two sets of embeddings.
    Returns shape (len_a, len_b).
    """
    norms_a = np.linalg.norm(matrix_a, axis=1, keepdims=True)
    norms_b = np.linalg.norm(matrix_b, axis=1, keepdims=True)
    matrix_a_norm = matrix_a / np.clip(norms_a, 1e-10, None)
    matrix_b_norm = matrix_b / np.clip(norms_b, 1e-10, None)
    return matrix_a_norm @ matrix_b_norm.T