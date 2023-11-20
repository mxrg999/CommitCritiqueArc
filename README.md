# GitHub Webhook Receiver

This project is a simple Flask application that receives webhook events from GitHub. It is designed to comment on new commits pushed to a specified repository.

## Vision and TODOs

- [x] Integrate AI to analyze and provide feedback on commits automatically.
- [x] Provide customization options for feedback types and levels based on user preferences.
- [ ] Create an easy-to-deploy server structure for quick setup.
   - [x] Create a docker-compose for running the script    
- [ ] Set up a CI/CD pipeline for automated testing and deployment of the webhook receiver service.

## Local Development Setup

To run this project locally, you'll need Python and `ngrok` installed on your development machine.

### Dependencies

- Python 3.6+
- Flask
- `python-dotenv`
- `requests`
- `Werkzeug`
- `openai`

### Installation

1. Clone this repository and navigate into the project directory.
2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   
   - Windows:

     ```
     venv\Scripts\activate
     ```

   - MacOS/Linux:

     ```
     source venv/bin/activate
     ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Set up your environment variables by copying the `.env.example` to `.env` and filling in the values.

### Running the Application

1. Start the Flask application:

   ```
   python app.py
   ```

2. In another terminal, start `ngrok` to create a tunnel to your local development server:

   ```
   ngrok http 5000
   ```

3. Copy the `ngrok` forwarding URL and use it as the payload URL in your GitHub repository webhook settings.

## Deployment

This application can be deployed to a cloud provider or a server that supports Python applications. Ensure environment variables are set up in your deployment environment.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under MIT license.
