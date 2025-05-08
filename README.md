# Minutes of Meeting AI Automation (MoM-AI)
- An AI-powered automated system that helps you manage your meeting lifecycle from start to finish. It captures your meetings, transcribes them using Whisper, diarizes speakers, summarizes using OpenAI, uploads to Google Drive, and emails participants.
  
## Table of contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Development Software & Tools](#development-software-&-tools)
- [Application Set Up Instructions](#application-set-up-instructions)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Sample Input/Output](#sample-input/output)
- 
## Features
- Auto-creates Google Drive folder when a Google Calendar events with attendees and Meet link is created
- Transcribe meeting audio using OpenAI Whisperr + WhisperX
- Identify speakers using pyannote-audio diarization
- Summarize discussions using LLMs (OpenAI GPT-4o-mini)
- Automatically store transcripts and summaries (google doc) in Google Drive
- share google doc with all attendees via email
- Uses Google Cloud Pub/Sub for scalable automation

## Tech Stack
- Python 3.10+
- Flask
- OpenAI API (GPT)
- Whisper
- pyannote-audio (for speaker diarization)
- Google APIs (Calendar, Drive, Docs, Gmail)
- Google Cloud Pub/Sub

## Development Software & Tools
- Python 3.9+
- Flask
- Visual Studio Code (VS Code)
- google cloud shell
- Git & GitHub
- OpenAI API
- Google Cloud Console
– Manage APIs, create OAuth credentials, monitor usage.
- Postman
- Ngrok
  
## Application Set Up Instructions

### Clone the Repository
```bash
git clone https://github.com/Akhila-89-ac/minutes-of-meeting-ai.git
cd minutes-of-meeting-ai

### Install Dependencies

pip install -r requirements.txt

### Set Up Google APIs
Go to Google Cloud Console

Create a new project

Enable these APIs:

Google Calendar API

Google Drive API

Google Docs API

Gmail API

Create OAuth 2.0 Client ID (Web/Desktop)

Download credentials.json and place it in the project root

On first run, you'll be prompted to authenticate, and token.json will be generated

4. Add Environment Variables
Create a .env file in the root:


OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8080/
EMAIL_SENDER=your_email@gmail.com

5. Set Up Google Cloud Pub/Sub
Create a Pub/Sub topic and a subscription

Set your Flask app's /webhook endpoint as the push endpoint

Grant the Pub/Sub service account permission to:

Push to your Flask endpoint

Read Google Calendar events

In pubsub_handler.py, configure the topic and subscription

## How to Use
✅ CLI Mode (default)

python app.py
This will:

Fetch the upcoming Google Calendar event

Create a folder in Google Drive (if not exists)

Wait for transcript.txt inside the folder

Summarize the transcript using GPT

Save the summary as summary.docx

Share the document with all meeting participants




## Sample Input/Output
🔊 Input
.wav or .mp3 meeting recording file in data/

📄 Output
output/transcript.txt → Whisper transcript

output/summary.txt → GPT-generated summary

Google Doc → Shared automatically with participants




