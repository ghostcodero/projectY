import os
import yt_dlp
import openai
import re
import requests


def download_audio():
    # Step 1: Ask for YouTube URL
    youtube_url = input("Enter the YouTube video URL: ")

    # Step 2: Define download options
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    output_template = os.path.join(download_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',  # High quality audio
        }],
        "quiet": True,
        "no_warnings": True  # Suppress warnings
    }

    # Step 3: Download and extract audio
    try:
        print("Downloading audio...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')

        print(f"Audio file saved to: {audio_file_path}")

    # we have to come back and fix for the case where the file size is larger than allowed by whisper: 
    # APIStatusError: Error code: 413 - {'error': {'message': '413: Maximum content size limit (26214400) exceeded (26423588 bytes read)', 
    #                                    'type': 'server_error', 'param': None, 'code': None}}

    except Exception as e:
        print(f"Error downloading video: {e}")
        exit(1)

    return audio_file_path

def transcribe_audio(file_path):
    """Sends an MP3 file to OpenAI's Whisper API and returns the transcription."""
    api_key = os.getenv("OPENAI_API_KEY")  # Load API key securely

    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    print("Transcribing audio...")

    client = openai.OpenAI(api_key=api_key)  # New API Client
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    transcript = response.text  # Updated response structure
    return transcript


def extract_predictions(transcript):
    """Sends the transcription to GPT-4-Turbo and extracts predictions as a Python list."""
    
    api_key = os.getenv("OPENAI_API_KEY")  # Load API key

    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    print("Analyzing transcript for predictions...")

     # Improved prompt to extract better predictions
    prompt = f"""
    You are analyzing a conversation transcript. Your goal is to extract **clear, concrete predictions about the future**, 
    avoiding vague or uncertain statements.

    **What counts as a prediction?**
    - Statements that clearly express **what will happen**, **what is expected**, or **likely future outcomes**.
    - Example phrases: "will happen," "is expected to," "is likely to," "is projected to," "experts predict that," "data suggests that."

    **What to ignore?**
    - Unclear or subjective statements (e.g., "it's not over," "maybe," "we will see").
    - General reflections, opinions, or past events.

    **Transcript:**
    {transcript}

    **Task:**
    - Extract **up to 10 of the most important predictions** in a numbered list.
    - Ensure that each prediction is **specific, meaningful, and clearly about the future**.
    - If no predictions are found, respond with: "No clear predictions were made in this conversation."

    **Response Format Example:**
    1. The team is expected to switch to a defensive strategy in the next game.
    2. Analysts predict that inflation will decrease by 2% next quarter.
    3. AI adoption in healthcare will grow significantly in the next five years.
    4. The player is likely to miss the next match due to injury.
    5. Scientists anticipate a major breakthrough in battery technology by 2030.
    """

    # Send the request to OpenAI's GPT-4-Turbo
    client = openai.OpenAI(api_key=api_key)
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
        print("❌ No clear predictions found.")
        return []

    print("\n✅ Extracted Predictions:")
    for p in predictions_list:
        print(f"- {p}")

    return predictions_list  # Returns a clean list of predictions


def generate_search_query(prediction):
    """Uses GPT-4o to generate an optimal Google search query for the given prediction."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
    You are an expert at crafting precise Google search queries.
    Your goal is to transform the given prediction into the **best possible search query** to find real-world results.

    **Prediction:** "{prediction}"

    **Instructions:**
    - Reformulate the prediction into a **high-quality search query** that will return useful information.
    - Focus on getting up-to-date news, results, or analysis relevant to the prediction.
    - Avoid unnecessary words or fluff.
    - if this is a sporting event you can use things like "final score OR match result OR who won" but reword naturally.

    **Example Conversions:**
    - Prediction: "Bitcoin will reach $100,000 in 2024."
      → Search Query: "Bitcoin price update 2024 latest news"
      
    - Prediction: "NASA will launch a manned Mars mission by 2030."
      → Search Query: "NASA Mars mission 2030 latest updates"

    **Return only the search query. No explanation needed.**
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that generates effective Google search queries."},
                  {"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response.choices[0].message.content.strip()


def search_google(prediction):
    """Search Google using SerpAPI with an optimized search query from GPT-4o."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SerpAPI key is missing. Set the SERPAPI_KEY environment variable.")

    # Generate an optimized search query
    optimized_query = generate_search_query(prediction)

    print(f"🔍 Searching Google for: {optimized_query}")

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
    return [result["snippet"] for result in search_results.get("organic_results", [])[:3]]  # Get top 3 snippets

def verify_prediction(prediction, search_snippets):
    """Use GPT-4o to verify if a prediction is TRUE, FALSE, UNCLEAR, or NOT YET,
       and extract the key event from search results."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
    You are verifying whether a prediction has come true using real-time Google search results.
    
    **Prediction:** "{prediction}"

    **Search Results:**
    {search_snippets}

    **Your Task:**
    1. **Summarize the key event from the search results** that confirms or contradicts the prediction. If the search results don't contain relevant details, say "No clear result found."
    2. **Classify the prediction as:**
       - **TRUE** → The event has definitively happened.
       - **FALSE** → The event did not happen.
       - **UNCLEAR** → There are conflicting sources, partial evidence, or no conclusive proof yet.
       - **NOT YET** → The event is in the future, and there is no evidence that it has happened.

    **Response Format Example:**
    Actual Result: "AZ Alkmaar won the game 1-0, contradicting the prediction."
    Rating: FALSE
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that verifies predictions using real-time Google search results."},
                  {"role": "user", "content": prompt}],
        max_tokens=150  # Increased token limit for a better response
    )

    return response.choices[0].message.content.strip()



#main loop


def main():
    audio_file = download_audio()
    
    transcribed_text = transcribe_audio (audio_file)
    
    prediction_list = extract_predictions (transcribed_text)

    verified_results = {}

    for prediction in prediction_list:
        print(f"\n🔍 Searching for: {prediction}")
        search_snippets = search_google(prediction)

        if not search_snippets:
            verified_results[prediction] = {
                "actual": "No relevant search results found.",
                "rating": "UNCLEAR"
            }
            continue

        print("\n🤖 Asking GPT-4o to verify...")
        gpt_response = verify_prediction(prediction, search_snippets)

        # Extracting structured response
        response_lines = gpt_response.split("\n")
        actual_result = response_lines[0].replace("Actual Result:", "").strip()
        rating = response_lines[-1].replace("Rating:", "").strip()

        verified_results[prediction] = {
            "actual": actual_result,
            "rating": rating
        }
    # Print the results in the requested format
    print("\n✅ Final Verified Predictions:\n")
    for i, (pred, details) in enumerate(verified_results.items(), start=1):
        print(f"Prediction {i}: {pred}")
        print(f"    Actual Result: {details['actual']}")
        print(f"    Rating: {details['rating']}\n")


if __name__ == "__main__":
    main()