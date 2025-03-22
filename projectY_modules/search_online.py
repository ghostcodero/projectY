import os
import openai
import requests
from projectY_modules import prompts


def generate_search_query(prediction):
    """Uses GPT-4o to generate an optimal Google search query for the given prediction."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

  
    client = openai.OpenAI(api_key=api_key)
    prompt = prompts.generate_search_query_prompt.format(prediction=prediction)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that generates effective Google search queries."},
                  {"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()


def search(prediction):
    """Search Google using SerpAPI with an optimized search query from GPT-4o."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SerpAPI key is missing. Set the SERPAPI_KEY environment variable.")

    # Generate an optimized search query
    optimized_query = generate_search_query(prediction)
    print(f'Searching Google with query: "{optimized_query}"\n')

    url = "https://serpapi.com/search"
    params = {
        "q": optimized_query,
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    search_results = response.json()

    snippets = []
    organic_results = search_results.get("organic_results", [])[:3]  # Top 3 results

    if not organic_results:
        print("No search result snippet found.\n")
        return snippets

    print("Search Results Found:")
    for i, result in enumerate(organic_results, 1):
        snippet = result.get("snippet")
        if not snippet:
            title = result.get("title", "No Title")
            link = result.get("link", "")
            snippet = f"{title} — {link}"

        print(f"{i}. {snippet}\n")
        snippets.append(snippet)

    return snippets

