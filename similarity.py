from sentence_transformers import SentenceTransformer
import numpy as np

def compute_embeddings(issues, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    texts = [f"{issue['summary']} {issue['description']}" for issue in issues]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

def compute_similarity_matrix(embeddings):
    # Normalize embeddings for cosine similarity
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    similarity_matrix = np.dot(norm_embeddings, norm_embeddings.T)
    return similarity_matrix
