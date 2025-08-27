import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

def extract_video_id(url):
    video_id = None
    if "youtu.be" in url:
        video_id = url.split("/")[-1]
        if "?" in video_id:
            video_id = video_id.split("?")[0]
    elif "youtube.com" in url and "v=" in url:
        video_id = url.split("v=")[1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]
    return video_id

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    custom_command = data.get('custom_command')
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY not found in environment variables.'}), 500

    if not youtube_url:
        return jsonify({'error': 'YouTube URL is missing.'}), 400

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        return jsonify({'error': f'Invalid API Key: {e}'}), 400

    try:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return jsonify({'error': 'Invalid or unsupported YouTube URL format.'}), 400

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        # Try to find a manual transcript in English, fallback to a generated one
        try:
            transcript_obj = transcript_list.find_manually_created_transcript(['en'])
        except:
            try:
                transcript_obj = transcript_list.find_generated_transcript(['en'])
            except:
                # If no English transcript is found, just take the first one
                transcript_obj = transcript_list[0]

        transcript_data = transcript_obj.fetch()
        transcript = " ".join([d.text for d in transcript_data])
    except Exception as e:
        return jsonify({'error': f'Error fetching transcript: {e}'}), 500

    prompt = f"""
    You are a YouTube video summarizer. You will be taking a transcript of a YouTube video and a command from the user.
    Your task is to provide a summary of the video based on the user's command.

    The command can specify:
    - The desired length of the summary (e.g., "short", "long").
    - The language of the summary (e.g., "Hindi", "English", "Hinglish").
    - The format of the summary (e.g., "bullet points", "essay", "paragraphs").

    Here is the transcript:
    ---
    {transcript}
    ---

    Here is the user's command:
    ---
    {custom_command}
    ---

    Please generate the summary based on the transcript and the command.
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        summary = response.text
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
