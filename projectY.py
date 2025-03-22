
from projectY_modules import downloader 
from projectY_modules import transcriber
from projectY_modules import prediction_extractor
from projectY_modules import prediction_verifier
from projectY_modules import search_online

import argparse
import sys

#main loop

import argparse
from projectY_modules import downloader, transcriber, prediction_extractor, prediction_verifier, search_online

def parse_args():
    parser = argparse.ArgumentParser(description="Verify predictions from YouTube or transcript.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--transcript", help="Path to a local transcript text file")
    group.add_argument("-u", "--url", help="YouTube video URL to download audio from")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def main():
    args = parse_args()
    verbose = args.verbose

    if args.transcript:
        with open(args.transcript, "r", encoding="utf-8") as f:
            transcribed_text = f.read()
        if verbose:
            print(f"[INFO] Loaded transcript from: {args.transcript}")

    elif args.url:
        if verbose:
            print(f"[INFO] Downloading audio from: {args.url}")
        audio_file = downloader.download_audio(args.url)
        transcribed_text = transcriber.transcribe_audio(audio_file, verbose=verbose)

    else:
        url = input("Enter the YouTube video URL: ")
        if verbose:
            print(f"[INFO] Downloading audio from: {url}")
        audio_file = downloader.download_audio(url)
        transcribed_text = transcriber.transcribe_audio(audio_file, verbose=verbose)

    prediction_list = prediction_extractor.extract_predictions(transcribed_text)
    verified_results = {}

    for prediction in prediction_list:
        print(f"\nPREDICTION: {prediction}")


        # search_snippets = search_online.search(prediction)

        # if not search_snippets:
        #     if verbose:
        #         print("[WARN] No search result snippet found.")
        #     verified_results[prediction] = {
        #         "actual": "No relevant search results found.",
        #         "rating": "UNCLEAR"
        #     }
        #     continue

        # if verbose:
        #     print("[INFO] Asking GPT-4o to verify...")

        if verbose:
            print("[INFO] Asking Perplexity to verify...")

        gpt_response = prediction_verifier.verify_prediction_with_perplexity(prediction)
        # Extracting structured response
        actual_result = "Not found"
        rating = "UNCLEAR"

        for line in gpt_response.splitlines():
            if line.strip().lower().startswith("actual result:"):
                actual_result = line.split(":", 1)[1].strip()
            elif line.strip().lower().startswith("rating:"):
                rating = line.split(":", 1)[1].strip()
        verified_results[prediction] = {
            "actual": actual_result,
            "rating": rating
        }

    # Final output
    print("\nFinal Verified Predictions:\n")
    for i, (pred, details) in enumerate(verified_results.items(), start=1):
        print(f"Prediction {i}: {pred}")
        print(f"    Actual Result: {details['actual']}")
        print(f"    Rating: {details['rating']}\n")


if __name__ == "__main__":
    main()