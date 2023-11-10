import requests
from openai import OpenAI


def handle_push_event(payload, github_api_token, openai_api_key):
    repo_full_name = payload['repository']['full_name']
    for commit in payload.get('commits', []):
        commit_sha = commit['id']
        comment = generate_comment(commit, openai_api_key)
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



import requests

def generate_comment(commit, openai_api_key):
    # API endpoint for the chat model
    chat_api_url = "https://api.openai.com/v1/chat/completions"

    # Extract necessary information from the commit
    commit_message = commit['message']
    author_name = commit['author']['name']

    # Define the messages for the chat
    messages = [
        {"role": "system", "content": "You are a helpful assistant providing feedback on GitHub commits."},
        {"role": "user", "content": f"A commit was made by {author_name} with the message '{commit_message}'. Can you provide some constructive feedback?"}
    ]

    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    try:
        response = requests.post(chat_api_url, json=data, headers=headers)
        response_json = response.json()
        ai_comment = response_json['choices'][0]['message']['content'].strip()
        return f"Hey @{author_name}! Here's some feedback on your commit: {ai_comment}"
    except Exception as e:
        print(f"Error while generating comment: {e}")
        return "Thank you for your commit!"
