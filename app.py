import os
import configparser
from flask import Flask, request, abort
import hmac
import hashlib
from webhook_handler import handle_push_event
from appcontext import AppContext

app = Flask(__name__)

app_context = AppContext()

# Read the configuration file
config_parser = configparser.ConfigParser()
config_parser.read('config/config.ini')

if app_context.response_type not in config_parser:
    print(f"Error: Response type '{app_context.response_type}' not found in config.ini")
    exit(1)

config_section = config_parser[app_context.response_type]

# Assuming AppContext is a class that encapsulates the app's context

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the signature from the request header
    signature_header = request.headers.get('X-Hub-Signature')

    # Compute the signature
    signature = hmac.new(app_context.github_secret, request.data, hashlib.sha1).hexdigest()

    # Validate the signature
    if not hmac.compare_digest(signature_header, 'sha1=' + signature):
        abort(403)

    # Handle the event
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == "push":
        handle_push_event(request.json, app_context, config_section)
        return '', 204
    else:
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
