import openai
import re
import logging
from projectY_modules import prompts
from projectY_modules.config import OPENAI_API_KEY

# Set up logger for this module
logger = logging.getLogger(__name__)

def extract_predictions(transcript, intro=""):
    """Sends the transcription to GPT-4-Turbo and extracts predictions as a Python list."""
    logger.info("Analyzing transcript for predictions...")
    logger.debug(f"Transcript length: {len(transcript)} characters")
    if intro:
        logger.debug(f"Using intro text of length: {len(intro)} characters")

    try:
        # Send the request to OpenAI's GPT-4-Turbo
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = prompts.extract_predictions_prompt.format(intro=intro, transcript=transcript)
        
        logger.debug("Sending request to GPT-4-Turbo...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant that analyzes transcripts."},
                      {"role": "user", "content": prompt}],
            max_tokens=400
        )
        logger.debug("Received response from GPT-4-Turbo")

        predictions_text = response.choices[0].message.content.strip()
        logger.debug(f"Raw predictions text: {predictions_text}")

        # Extract predictions using regex to capture numbered list format
        predictions_list = re.findall(r"\d+\.\s*(.*)", predictions_text)
        logger.debug(f"Found {len(predictions_list)} predictions")

        if not predictions_list:
            logger.warning("No clear predictions found in the transcript")
            return []

        logger.info(f"Successfully extracted {len(predictions_list)} predictions")
        return predictions_list  # Returns a clean list of predictions

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during prediction extraction: {str(e)}", exc_info=True)
        raise