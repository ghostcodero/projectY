import os
import openai

def transcribe_audio(file_path):
    """Sends an MP3 file to OpenAI's Whisper API and returns the transcription."""
    api_key = os.getenv("OPENAI_API_KEY")  # Load API key securely

    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    print("Transcribing audio...")

    client = openai.OpenAI(api_key=api_key)  # New API Client
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    transcript = response.text  # Updated response structure
    return transcript