import configparser
import os
from dotenv import load_dotenv

class AppContext:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config/config.ini')

        load_dotenv()
        self.github_secret = os.environ.get('GITHUB_SECRET').encode()
        self.github_api_token = os.getenv('GITHUB_API_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.response_type = os.environ.get('RESPONSE_TYPE', 'KindResponse')
