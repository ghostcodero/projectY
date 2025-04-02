import openai
import json
import requests
from projectY_modules import prompts
from projectY_modules.config import OPENAI_API_KEY, PERPLEXITY_API_KEY


def verify_prediction(prediction, search_snippets):
    """Use GPT-4o to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET,
       and extract the key event from search results."""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = prompts.verify_prediction_prompt.format(prediction=prediction, search_snippets=search_snippets)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that verifies predictions using real-time Google search results."},
                  {"role": "user", "content": prompt}],
        max_tokens=150  # Increased token limit for a better response
    )

    return response.choices[0].message.content.strip()

def verify_prediction_with_perplexity(prediction, verbose):
    """Use Perplexity API to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET."""
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Prompt string from prompts.py
    prompt_text = prompts.verify_prediction_prompt_perplexity.format(prediction=prediction)

    payload = {
        "model": "sonar-reasoning-pro",  # <- try this model; pplx-7b-online is deprecated in some accounts
        "messages": [
            {"role": "system", "content": "You are a helpful AI that verifies predictions using current web knowledge."},
            {"role": "user", "content": prompt_text}
        ]
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        response_text = response.json()["choices"][0]["message"]["content"]
        if (verbose):
            print(response_text)  # Debug: see the full raw response
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as e:
        print("[ERROR] Perplexity API returned an error.")
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        raise e