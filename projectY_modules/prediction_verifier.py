import os
import openai

from projectY_modules import prompts


def verify_prediction(prediction, search_snippets):
    """Use GPT-4o to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET,
       and extract the key event from search results."""
    api_key = os.getenv("OPENAI_API_KEY")


    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)
    prompt = prompts.verify_prediction_prompt.format(prediction=prediction, search_snippets=search_snippets)


    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that verifies predictions using real-time Google search results."},
                  {"role": "user", "content": prompt}],
        max_tokens=150  # Increased token limit for a better response
    )

    return response.choices[0].message.content.strip()
