from sklearn.cluster import AgglomerativeClustering
import numpy as np

def cluster_issues(embeddings, issues, similarity_threshold=0.80):
    clustering = AgglomerativeClustering(
        n_clusters=None,
        affinity='cosine',
        linkage='average',
        distance_threshold=1 - similarity_threshold
    )
    labels = clustering.fit_predict(embeddings)
    clusters = {}
    for label, issue in zip(labels, issues):
        clusters.setdefault(label, []).append(issue['id'])
    return list(clusters.values())
