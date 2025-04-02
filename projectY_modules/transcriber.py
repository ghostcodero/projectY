import os
import openai
import logging
import pydub
from projectY_modules.config import OPENAI_API_KEY

# Set up logger for this module
logger = logging.getLogger(__name__)

# Whisper API file size limit (25MB)
WHISPER_MAX_FILE_SIZE = 25 * 1024 * 1024

def transcribe_audio(file_path):
    """Sends an MP3 file to OpenAI's Whisper API, saves the transcript, and returns it."""
    logger.info("Starting audio transcription...")
    
    try:
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > WHISPER_MAX_FILE_SIZE:
            logger.warning(f"File size ({file_size/1024/1024:.2f}MB) exceeds Whisper API limit of 25MB")
            logger.info("Attempting to split and transcribe file in chunks...")
            return transcribe_large_file(file_path)
        
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

def transcribe_large_file(file_path):
    """Handle transcription of large files by splitting them into chunks."""
    try:
        # Load the audio file
        audio = pydub.AudioSegment.from_mp3(file_path)
        
        # Calculate chunk size (20MB to leave some buffer)
        chunk_size = 20 * 1024 * 1024
        chunk_length_ms = int(chunk_size / (audio.frame_rate * audio.channels * audio.sample_width / 1000))
        
        # Split into chunks
        chunks = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunks.append(chunk)
        
        logger.info(f"Split audio into {len(chunks)} chunks")
        
        # Transcribe each chunk
        full_transcript = []
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        for i, chunk in enumerate(chunks, 1):
            # Export chunk to temporary file
            chunk_path = f"{file_path}.chunk{i}.mp3"
            chunk.export(chunk_path, format="mp3")
            
            try:
                logger.debug(f"Transcribing chunk {i}/{len(chunks)}")
                with open(chunk_path, "rb") as chunk_file:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=chunk_file
                    )
                full_transcript.append(response.text)
            finally:
                # Clean up temporary chunk file
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
        
        # Combine transcripts
        transcript = " ".join(full_transcript)
        
        # Save full transcript
        os.makedirs("transcripts", exist_ok=True)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        transcript_path = os.path.join("transcripts", f"{base_name}.txt")
        
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        logger.info(f"Full transcript saved to: {transcript_path}")
        return transcript
        
    except Exception as e:
        logger.error(f"Error processing large file: {str(e)}")
        raise
