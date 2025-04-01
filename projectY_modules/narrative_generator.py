import os
import openai
from projectY_modules import prompts

def generate_narrative(video_title, intro_text, verified_results, verbose=False):
    """Generates a podcast-style narrative summarizing the predictions, outcomes, and ratings."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = openai.OpenAI(api_key=api_key)

    # Format the prediction results into readable markdown-style bullets
    prediction_blocks = ""
    for i, (prediction, details) in enumerate(verified_results.items(), start=1):
        prediction_blocks += f"Prediction {i}: {prediction}\n"
        prediction_blocks += f"    Actual Result: {details['actual']}\n"
        prediction_blocks += f"    Rating: {details['rating']}\n\n"

    # Build the narrative generation prompt
    prompt = prompts.generate_narrative_prompt.format(
        video_title=video_title,
        intro_text=intro_text or "",
        predictions_block=prediction_blocks.strip()
    )

    if verbose:
        print("[INFO] Sending narrative generation prompt to GPT...")

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a podcast script writer that transforms prediction analysis into engaging narratives."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000  # Can increase if needed
    )

    return response.choices[0].message.content.strip()
