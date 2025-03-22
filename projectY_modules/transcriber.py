import os
import openai

def transcribe_audio(file_path):
    """Sends an MP3 file to OpenAI's Whisper API, saves the transcript, and returns it."""
    api_key = os.getenv("OPENAI_API_KEY")  # Load API key securely

    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    print("Transcribing audio...")

    client = openai.OpenAI(api_key=api_key)
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

    print(f"Transcript saved to: {transcript_path}")

    return transcript
