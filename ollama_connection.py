import requests
import json
import os

class OllamaConnection:
    def __init__(self, config_section):
        self.model = os.getenv('OLLAMA_MODEL', 'llama2')
        self.system_message = config_section['system_message']
        self.user_message_template = config_section['user_message']
        self.url = 'http://saturn-cortex:11434/api/generate'
        self.options = None  # Set appropriate options if needed

    def generate_comment(self, commit):
        author_name = commit['author']['name']
        commit_message = commit['message']
        prompt = self.user_message_template.format(author_name=author_name, commit_message=commit_message)
        data = {
            'model': self.model,
            'prompt': prompt,
            'options': self.options,
            'stream': False
        }
        try:
            response = requests.post(self.url, json=data)
            if response.status_code == 200:
                response_json = response.json()
                if 'response' in response_json:
                    return f"[CommitCritiqueArc](https://github.com/mxrg999/CommitCritiqueArc):\n {response_json['response']}"
                else:
                    return "Response from Ollama lacks 'response' key."
            else:
                print(f"Ollama request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error while generating comment with Ollama: {e}")
            return None
