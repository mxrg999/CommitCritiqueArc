from flask import Flask, request, abort
from webhook_handler import handle_push_event
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    github_secret = os.environ.get('GITHUB_SECRET').encode()

    # Validate payload from GitHub
    # ... validation logic here ...

    # Handle the event
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == "push":
        handle_push_event(request.json)
        return '', 204
    else:
        # For now, only push events
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
