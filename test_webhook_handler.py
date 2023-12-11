import unittest
from unittest.mock import patch, MagicMock
from webhook_handler import handle_push_event, comment_on_commit

class TestWebhookHandler(unittest.TestCase):

    def setUp(self):
        # Set up any common data for the tests
        self.payload = {
            'repository': {'full_name': 'test/repo'},
            'commits': [{'id': '12345', 'author': {'name': 'TestAuthor'}, 'message': 'Test commit message'}]
        }
        self.app_context = MagicMock()  # Mock the app_context
        self.config_section = {'system_message': 'Test', 'user_message': 'Test message'}




    @patch('webhook_handler.OpenAIConnection')
    @patch('webhook_handler.requests.post')
    def test_successful_comment_openai(self, mock_post, mock_openai_connection):
        # Mock OpenAI response
        mock_openai_connection.return_value.generate_comment.return_value = "OpenAI Test Comment"

        # Mock POST request to GitHub API
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Set environment variable to use OpenAI
        with patch.dict('os.environ', {'AI_SERVICE': 'OpenAI'}):
            handle_push_event(self.payload, self.app_context, self.config_section)

        # Assert that the GitHub API was called with the expected comment
        mock_post.assert_called_with(
            'https://api.github.com/repos/test/repo/commits/12345/comments',
            json={'body': "OpenAI Test Comment"},
            headers=ANY
        )
    
    @patch('webhook_handler.OllamaConnection')
    @patch('webhook_handler.requests.post')
    def test_successful_comment_ollama(self, mock_post, mock_ollama_connection):
        # Mock Ollama response
        mock_ollama_connection.return_value.generate_comment.return_value = "Ollama Test Comment"

        # Mock POST request to GitHub API
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Set environment variable to use Ollama
        with patch.dict('os.environ', {'AI_SERVICE': 'Ollama'}):
            handle_push_event(self.payload, self.app_context, self.config_section)

        # Assert that the GitHub API was called with the expected comment
        mock_post.assert_called_with(
            'https://api.github.com/repos/test/repo/commits/12345/comments',
            json={'body': "Ollama Test Comment"},
            headers=ANY
        )


# 
if __name__ == '__main__':
    unittest.main()
    # 


