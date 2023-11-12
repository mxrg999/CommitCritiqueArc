import requests
from openai import OpenAI
from appcontext import AppContext
from openai_connection import OpenAIConnection



def handle_push_event(payload, app_context, config_section):
    openai_connection = OpenAIConnection(app_context.openai_api_key, config_section)

    repo_full_name = payload['repository']['full_name']
    for commit in payload.get('commits', []):
        commit_sha = commit['id']
        comment = openai_connection.generate_comment(commit)
        response = comment_on_commit(commit_sha, repo_full_name, comment, app_context.github_api_token)

        if response.status_code != 201:
            print(f"Failed to post comment on {commit_sha}. Status code: {response.status_code}")
        else:
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