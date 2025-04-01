import os
import openai
import re

from projectY_modules import prompts

def extract_predictions(transcript, verbose, intro=""):
    """Sends the transcription to GPT-4-Turbo and extracts predictions as a Python list."""
    
    api_key = os.getenv("OPENAI_API_KEY")  # Load API key

    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    if (verbose):
        print("Analyzing transcript for predictions...")

     # Send the request to OpenAI's GPT-4-Turbo
    client = openai.OpenAI(api_key=api_key)
    prompt = prompts.extract_predictions_prompt.format(intro=intro, transcript=transcript)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are an AI assistant that analyzes transcripts."},
                  {"role": "user", "content": prompt}],
        max_tokens=400
    )

    predictions_text = response.choices[0].message.content.strip()

    # Extract predictions using regex to capture numbered list format
    predictions_list = re.findall(r"\d+\.\s*(.*)", predictions_text)

    if not predictions_list:
        if (verbose):
            print("No clear predictions found.")
        return []

    return predictions_list  # Returns a clean list of predictions