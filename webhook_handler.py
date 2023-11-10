import requests

def handle_push_event(payload, github_api_token):
    # Log the entire payload for debugging
    print("Received payload:", payload)

    for commit in payload.get('commits', []):
        commit_url = commit['url']
        comment = "Your automated comment here"

        print(f"Attempting to post comment on commit: {commit_url}")
        response = comment_on_commit(commit_url, comment, github_api_token)

        if response.status_code != 201:
            print(f"Failed to post comment on {commit_url}. Status code: {response.status_code}")
        else:
            print(f"Successfully posted comment on {commit_url}. Response: {response.json()}")

def comment_on_commit(commit_url, comment, github_api_token):
    # Construct the GitHub API URL to post a comment on a commit
    comments_url = f"{commit_url}/comments"

    print(f"Posting to URL: {comments_url}")

    headers = {
        'Authorization': f'token {github_api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'body': comment}
    
    response = requests.post(comments_url, json=data, headers=headers)

    # Log the response for debugging
    print(f"GitHub API Response: {response.status_code}, {response.text}")

    return response
