import os
import openai
from projectY_modules.config import OPENAI_API_KEY

def transcribe_audio(file_path, verbose):
    """Sends an MP3 file to OpenAI's Whisper API, saves the transcript, and returns it."""
    if (verbose):
        print("Transcribing audio...")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    transcript = response.text

    # Create transcripts directory if it doesn't exist
    os.makedirs("transcripts", exist_ok=True)

    # Build transcript filename based on audio file name
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    transcript_path = os.path.join("transcripts", f"{base_name}.txt")

    # Save transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    if (verbose):
        print(f"Transcript saved to: {transcript_path}")

    return transcript
