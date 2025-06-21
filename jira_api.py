import requests

def fetch_jira_issues(base_url, project_key, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json"
    }
    issues = []
    start_at = 0
    max_results = 100
    while True:
        params = {
            'jql': f'project={project_key}',
            'startAt': start_at,
            'maxResults': max_results,
            'fields': 'summary,description'
        }
        response = requests.get(
            f"{base_url}/rest/api/2/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        issues.extend(data['issues'])
        if len(data['issues']) < max_results:
            break
        start_at += max_results
    # Extract (id, summary, description)
    return [
        {
            'id': issue['key'],
            'summary': issue['fields']['summary'],
            'description': issue['fields'].get('description', '')
        }
        for issue in issues
    ]
