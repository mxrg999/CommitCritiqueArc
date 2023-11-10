from flask import Flask, request, abort
from webhook_handler import handle_push_event
import os
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Retrieve the secret from the environment
    github_secret = os.environ.get('GITHUB_SECRET').encode()

    # Get the signature from the request header
    signature_header = request.headers.get('X-Hub-Signature')

    # Compute the signature
    signature = hmac.new(github_secret, request.data, hashlib.sha1).hexdigest()

    # Validate the signature
    if not hmac.compare_digest(signature_header, 'sha1=' + signature):
        abort(403)  # Abort if the signature is not valid
    
    
    github_api_token = os.getenv('GITHUB_API_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')


    # Handle the event
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == "push":
        handle_push_event(request.json, github_api_token, openai_api_key)
        return '', 204
    else:
        # For now, only push events
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
