import openai
import logging
from projectY_modules import prompts
from projectY_modules.config import OPENAI_API_KEY

# Set up logger for this module
logger = logging.getLogger(__name__)

def generate_narrative(video_title, intro_text, verified_results):
    """Generates a podcast-style narrative summarizing the predictions, outcomes, and ratings."""
    logger.info(f"Generating narrative for video: {video_title}")
    logger.debug(f"Number of predictions to summarize: {len(verified_results)}")

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        # Format the prediction results into readable markdown-style bullets
        prediction_blocks = ""
        for i, (prediction, details) in enumerate(verified_results.items(), start=1):
            prediction_blocks += f"Prediction {i}: {prediction}\n"
            prediction_blocks += f"    Actual Result: {details['actual']}\n"
            prediction_blocks += f"    Rating: {details['rating']}\n\n"
        
        logger.debug("Formatted prediction blocks for narrative")

        # Build the narrative generation prompt
        prompt = prompts.generate_narrative_prompt.format(
            video_title=video_title,
            intro_text=intro_text or "",
            predictions_block=prediction_blocks.strip()
        )
        logger.debug("Built narrative generation prompt")

        logger.info("Sending narrative generation prompt to GPT-4-Turbo...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a podcast script writer that transforms prediction analysis into engaging narratives."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000  # Can increase if needed
        )
        logger.debug("Received response from GPT-4-Turbo")
        
        narrative = response.choices[0].message.content.strip()
        logger.info("Successfully generated narrative")
        logger.debug(f"Narrative length: {len(narrative)} characters")
        
        return narrative

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during narrative generation: {str(e)}", exc_info=True)
        raise
