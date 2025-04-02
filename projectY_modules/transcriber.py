import os
import openai
import logging
from projectY_modules.config import OPENAI_API_KEY

# Set up logger for this module
logger = logging.getLogger(__name__)

def transcribe_audio(file_path):
    """Sends an MP3 file to OpenAI's Whisper API, saves the transcript, and returns it."""
    logger.info("Starting audio transcription...")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        with open(file_path, "rb") as audio_file:
            logger.debug(f"Sending {file_path} to Whisper API")
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcript = response.text
        logger.debug("Received transcript from Whisper API")

        # Create transcripts directory if it doesn't exist
        os.makedirs("transcripts", exist_ok=True)

        # Build transcript filename based on audio file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        transcript_path = os.path.join("transcripts", f"{base_name}.txt")

        # Save transcript
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        logger.info(f"Transcript saved to: {transcript_path}")
        return transcript

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    except IOError as e:
        logger.error(f"File operation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during transcription: {str(e)}")
        raise
