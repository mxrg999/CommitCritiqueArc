import requests
from openai import OpenAI

class OpenAIConnection:
    def __init__(self, api_key, config_section):
        self.api_key = api_key
        self.chat_api_url = "https://api.openai.com/v1/chat/completions"
        self.system_message = config_section['system_message']
        self.user_message_template = config_section['user_message']

    def generate_comment(self, commit):
        author_name = commit['author']['name']
        commit_message = commit['message']
        user_message = self.user_message_template.format(author_name=author_name, commit_message=commit_message)

        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message}
        ]

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }

        try:
            response = requests.post(self.chat_api_url, json=data, headers=headers)
            response_json = response.json()
            ai_comment = response_json['choices'][0]['message']['content'].strip()
            return f"[CommitCritiqueArc](https://github.com/mxrg999/CommitCritiqueArc): {ai_comment}"
        except Exception as e:
            print(f"Error while generating comment: {e}")
            return "Thank you for your commit!"
