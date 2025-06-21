from clustering import cluster_issues
import numpy as np

def test_clustering():
    emb = np.array([
        [1.0, 0.0],
        [0.99, 0.01],
        [0.0, 1.0]
    ])
    fake_issues = [
        {'id': 'PROJ-1'}, {'id': 'PROJ-2'}, {'id': 'PROJ-3'}
    ]
    clusters = cluster_issues(emb, fake_issues, similarity_threshold=0.95)
    grouped = [set(g) for g in clusters]
    assert any({'PROJ-1', 'PROJ-2'} == g for g in grouped)
    assert any({'PROJ-3'} == g for g in grouped)
