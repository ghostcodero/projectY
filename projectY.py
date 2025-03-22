
from projectY_modules import downloader 
from projectY_modules import transcriber
from projectY_modules import prediction_extractor
from projectY_modules import prediction_verifier
from projectY_modules import search_online

#main loop

def main():
    audio_file = downloader.download_audio()
    
    transcribed_text = transcriber.transcribe_audio (audio_file)
    
    prediction_list = prediction_extractor.extract_predictions (transcribed_text)

    verified_results = {}

    for prediction in prediction_list:
        print(f"\nSearching for: {prediction}")
        search_snippets = search_online.search(prediction)

        if not search_snippets:
            verified_results[prediction] = {
                "actual": "No relevant search results found.",
                "rating": "UNCLEAR"
            }
            continue

        print("\nAsking GPT-4o to verify...")
        gpt_response = prediction_verifier.verify_prediction(prediction, search_snippets)

        # Extracting structured response
        response_lines = gpt_response.split("\n")
        actual_result = response_lines[0].replace("Actual Result:", "").strip()
        rating = response_lines[-1].replace("Rating:", "").strip()

        verified_results[prediction] = {
            "actual": actual_result,
            "rating": rating
        }
    # Print the results in the requested format
    print("\nFinal Verified Predictions:\n")
    for i, (pred, details) in enumerate(verified_results.items(), start=1):
        print(f"Prediction {i}: {pred}")
        print(f"    Actual Result: {details['actual']}")
        print(f"    Rating: {details['rating']}\n")


if __name__ == "__main__":
    main()