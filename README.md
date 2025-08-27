# YouTube Video Summarizer

This is a simple web application that uses the YouTube Transcript API and Google's Gemini API to summarize YouTube videos.

## Features

- Fetches transcripts from YouTube videos.
- Uses the Gemini API to generate summaries based on user commands.
- Allows users to specify summary length, language, and format.
- Securely handles the Gemini API key using environment variables.

## Setup and Usage

Follow these steps to run the application locally.

### 1. Clone the Repository

Clone this repository to your local machine.

### 2. Create a Virtual Environment

It is recommended to use a Python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```
_On Windows, use `venv\\Scripts\\activate`_

### 3. Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
```

### 4. Set Your API Key

The application requires a Google Gemini API key. It loads the key from a `.env` file.

- Make a copy of the example file `.env.example` and name it `.env`.
- Open the `.env` file and replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key.

```
# .env file
GEMINI_API_KEY="AIza..................."
```

### 5. Run the Application

Start the Flask development server.

```bash
python app.py
```

The application will be available at `http://1227.0.0.1:5000`. Open this URL in your web browser.