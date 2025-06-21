from similarity import compute_embeddings, compute_similarity_matrix
import numpy as np

def test_similarity():
    fake_issues = [
        {"id": "PROJ-1", "summary": "Login button broken", "description": "Clicking login fails"},
        {"id": "PROJ-2", "summary": "Login fails", "description": "Button does not work"},
        {"id": "PROJ-3", "summary": "Cosmetic issue", "description": "Minor color difference"}
    ]
    embeddings = compute_embeddings(fake_issues)
    sim_matrix = compute_similarity_matrix(embeddings)
    assert sim_matrix.shape == (3, 3)
    assert sim_matrix[0, 1] > sim_matrix[0, 2]
    assert sim_matrix[0, 1] > sim_matrix[1, 2]
