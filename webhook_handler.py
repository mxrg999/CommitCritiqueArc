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



def generate_comment(commit, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    # Extract necessary information from the commit
    commit_message = commit['message']
    author_name = commit['author']['name']
    commit_url = commit['url']

    # Define the prompt for the AI
    prompt = f"A commit was made by {author_name} with the message '{commit_message}'. " \
             "Provide a constructive comment about the commit."

    # Call the OpenAI API
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-1106",
            prompt=prompt,
            max_tokens=150
        )
        ai_comment = response.choices[0].text.strip()
        return f"Hey @{author_name}! Here's some feedback on your commit: {ai_comment}\nCommit URL: {commit_url}"
    except Exception as e:
        print(f"Error while generating comment: {e}")
        return "Thank you for your commit!"
