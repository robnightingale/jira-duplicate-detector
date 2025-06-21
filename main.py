from jira_api import fetch_jira_issues
from similarity import compute_embeddings
from clustering import cluster_issues

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

if __name__ == "__main__":
    main()
