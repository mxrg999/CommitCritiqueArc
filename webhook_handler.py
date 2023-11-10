import requests

def handle_push_event(payload, github_api_token):
    # Iterate through commits and post a comment
    for commit in payload.get('commits', []):
        commit_url = commit['url']
        comment = "Your automated comment here"
        comment_on_commit(commit_url, comment, github_api_token)

def comment_on_commit(commit_url, comment, github_api_token):
    headers = {'Authorization': f'token {github_api_token}'}
    data = {'body': comment}
    response = requests.post(commit_url, json=data, headers=headers)
    return response