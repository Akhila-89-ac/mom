from flask import Flask, redirect, request
import os
import json
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

# Load environment variables
load_dotenv("/home/akhila8452/mom_auth/.env")


# Tell oauthlib to allow http (just for development with ngrok)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'






app = Flask(__name__)

# Get environment variables
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = os.getenv("GOOGLE_SCOPES").split()

# Validate env variables
if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("❌ One or more environment variables are missing.")

# Configure the OAuth2 flow
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI]
        }
    },
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route('/')
def index():
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials

        # Save credentials to token.json
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())

        return '✅ Authentication successful! Token saved to token.json'

    except Exception as e:
        import traceback
        return f'❌ Error occurred:<br><pre>{traceback.format_exc()}</pre>', 500

if __name__ == '__main__':
    app.run('0.0.0.0', port=8081)
