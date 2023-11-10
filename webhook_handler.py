import requests

def handle_push_event(payload, github_api_token):
    # Iterate through commits and post a comment
    for commit in payload.get('commits', []):
        commit_url = commit['url']
        comment = "Your automated comment here"
        comment_on_commit(commit_url, comment, github_api_token)




def comment_on_commit(commit_url, comment, github_api_token):
    # GitHub API URL to post a comment on a commit
    comments_url = f"{commit_url}/comments"

    headers = {
        'Authorization': f'token {github_api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'body': comment}
    
    response = requests.post(comments_url, json=data, headers=headers)
    return response
