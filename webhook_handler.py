import requests

def handle_push_event(payload, github_api_token):
    repo_full_name = payload['repository']['full_name']
    for commit in payload.get('commits', []):
        commit_sha = commit['id']
        comment = generate_comment(commit)
        response = comment_on_commit(commit_sha, repo_full_name, comment, github_api_token)

        if response.status_code != 201:
            print(f"Failed to post comment on {commit_sha}. Status code: {response.status_code}")
        else:
            # print(f"Successfully posted comment on {commit_sha}. Response: {response.json()}")
            print(f"Successfully posted comment on {commit_sha}")


def comment_on_commit(commit_sha, repo_full_name, comment, github_api_token):
    # Correct API URL for posting a comment
    comments_url = f"https://api.github.com/repos/{repo_full_name}/commits/{commit_sha}/comments"

    headers = {
        'Authorization': f'token {github_api_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'body': comment}
    response = requests.post(comments_url, json=data, headers=headers)
    return response


def generate_comment(commit):
    # Get the commit message
    commit_message = commit['message']

    # Get the author name
    author_name = commit['author']['name']

    # Get the commit URL
    commit_url = commit['url']

    # Generate the comment
    comment = f"Hey @{author_name}! I noticed that your commit message is '{commit_message}'. " \
              f"Please remember to follow the commit message guidelines: " \
              f"Do's: https://chris.beams.io/posts/git-commit/#do " \
    
    return comment