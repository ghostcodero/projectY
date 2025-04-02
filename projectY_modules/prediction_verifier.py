import openai
import json
import requests
import logging
from projectY_modules import prompts
from projectY_modules.config import OPENAI_API_KEY, PERPLEXITY_API_KEY

# Set up logger for this module
logger = logging.getLogger(__name__)

def verify_prediction(prediction, search_snippets):
    """Use GPT-4o to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET,
       and extract the key event from search results."""
    logger.debug(f"Verifying prediction with GPT-4o: {prediction}")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = prompts.verify_prediction_prompt.format(prediction=prediction, search_snippets=search_snippets)
        
        logger.debug("Sending request to GPT-4o...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an AI that verifies predictions using real-time Google search results."},
                      {"role": "user", "content": prompt}],
            max_tokens=150  # Increased token limit for a better response
        )
        logger.debug("Received response from GPT-4o")
        
        result = response.choices[0].message.content.strip()
        logger.debug(f"Verification result: {result}")
        return result

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during GPT-4o verification: {str(e)}", exc_info=True)
        raise

def verify_prediction_with_perplexity(prediction):
    """Use Perplexity API to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET."""
    logger.info(f"Verifying prediction with Perplexity: {prediction}")
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Prompt string from prompts.py
    prompt_text = prompts.verify_prediction_prompt_perplexity.format(prediction=prediction)
    logger.debug(f"Using prompt: {prompt_text}")

    payload = {
        "model": "sonar-reasoning-pro",  # <- try this model; pplx-7b-online is deprecated in some accounts
        "messages": [
            {"role": "system", "content": "You are a helpful AI that verifies predictions using current web knowledge."},
            {"role": "user", "content": prompt_text}
        ]
    }

    try:
        logger.debug("Sending request to Perplexity API...")
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        response_text = response.json()["choices"][0]["message"]["content"]
        logger.debug(f"Raw Perplexity response: {response_text}")
        logger.info("Successfully received verification from Perplexity")
        
        return response_text.strip()

    except requests.exceptions.HTTPError as e:
        logger.error(f"Perplexity API error: Status code {response.status_code}")
        logger.error(f"Response text: {response.text}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while calling Perplexity API: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during Perplexity verification: {str(e)}", exc_info=True)
        raise