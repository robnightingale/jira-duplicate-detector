from jira_api import fetch_jira_issues
from similarity import compute_embeddings
from clustering import cluster_issues

import pandas as pd

def export_clusters_csv(clusters, issues, filename="clusters.csv"):
    # Make a map of id -> (summary, description)
    issue_map = {issue['id']: issue for issue in issues}
    rows = []
    for cluster_id, group in enumerate(clusters):
        if len(group) < 2:
            continue  # skip singleton clusters
        for issue_id in group:
            issue = issue_map[issue_id]
            rows.append({
                'cluster_id': cluster_id,
                'issue_id': issue['id'],
                'summary': issue['summary'],
                'description': issue['description'],
            })
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    print(f"Clusters exported to {filename}")

import networkx as nx
import matplotlib.pyplot as plt

def visualize_clusters(clusters, issues):
    G = nx.Graph()
    issue_map = {issue['id']: issue['summary'] for issue in issues}

    for group in clusters:
        if len(group) < 2:
            continue
        # Make fully connected subgraph for each cluster
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                G.add_edge(group[i], group[j], cluster=True)
        for issue_id in group:
            G.nodes[issue_id]['label'] = issue_map.get(issue_id, '')

    pos = nx.spring_layout(G, k=0.8)
    plt.figure(figsize=(12,8))
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Jira Issue Clusters (Connected = similar)")
    plt.axis('off')
    plt.show()

    import json

def export_clusters_json(clusters, issues, filename="clusters.json"):
    issue_map = {issue['id']: issue for issue in issues}
    output = []
    for group in clusters:
        if len(group) < 2:
            continue
        group_data = [issue_map[issue_id] for issue_id in group]
        output.append(group_data)
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Clusters exported to {filename}")


def main():
    # --- Config: Replace these! ---
    JIRA_BASE = "https://yourinstance.atlassian.net"
    JIRA_PROJECT = "PROJ"
    JIRA_TOKEN = "YOUR_JIRA_API_TOKEN"

    # 1. Download issues
    issues = fetch_jira_issues(JIRA_BASE, JIRA_PROJECT, JIRA_TOKEN)
    print(f"Fetched {len(issues)} tickets.")

    # 2. Embed each ticket
    embeddings = compute_embeddings(issues)

    # 3. Cluster tickets
    clusters = cluster_issues(embeddings, issues, similarity_threshold=0.83)

    print("Potential duplicate clusters:")
    for group in clusters:
        if len(group) > 1:
            print(group)

    # After printing clusters
    export_clusters_csv(clusters, issues)

if __name__ == "__main__":
    main()


