from projectY_modules import config
from projectY_modules import downloader 
from projectY_modules import transcriber
from projectY_modules import prediction_extractor
from projectY_modules import prediction_verifier
from projectY_modules import narrative_generator

import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Verify predictions from YouTube or transcript.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--transcript", help="Path to a local transcript text file")
    group.add_argument("-u", "--url", help="YouTube video URL to download audio from")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--intro-file", type=str, help="Optional path to a file with introductory context for the transcript.")
    return parser.parse_args()

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = parse_args()
    verbose = args.verbose
    intro_text = ""
    video_title = "Unknown Video"

    if args.transcript:
        with open(args.transcript, "r", encoding="utf-8") as f:
            transcribed_text = f.read()
        if verbose:
            print(f"[INFO] Loaded transcript from: {args.transcript}")

        video_title = os.path.splitext(os.path.basename(args.transcript))[0]

    elif args.url:
        if verbose:
            print(f"[INFO] Downloading audio from: {args.url}")
        audio_file = downloader.download_audio(args.url, verbose)
        transcribed_text = transcriber.transcribe_audio(audio_file, verbose=verbose)
        video_title = os.path.splitext(os.path.basename(audio_file))[0]

    else:
        url = input("Enter the YouTube video URL: ")
        if verbose:
            print(f"[INFO] Downloading audio from: {url}")
        audio_file = downloader.download_audio(url, verbose)
        transcribed_text = transcriber.transcribe_audio(audio_file, verbose=verbose)
        video_title = os.path.splitext(os.path.basename(audio_file))[0]

    if args.intro_file:
        if os.path.exists(args.intro_file):
            with open(args.intro_file, "r", encoding="utf-8") as f:
                intro_text = f.read().strip()
            if verbose:
                print(f"[INFO] Loaded intro from: {args.intro_file}")
        else:
            print(f"[WARN] Intro file not found: {args.intro_file}")

    prediction_list = prediction_extractor.extract_predictions(transcribed_text, intro=intro_text, verbose=verbose)
    verified_results = {}

    for prediction in prediction_list:
        if (verbose):
            print(f"\nPREDICTION: {prediction}")
            print("[INFO] Asking Perplexity to verify...")

        gpt_response = prediction_verifier.verify_prediction_with_perplexity(prediction, verbose=verbose)
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

    print(f"#####################################################")
    print("\n#######     Final Verified Predictions     ##########\n")
    print(f"#####################################################")
    for i, (pred, details) in enumerate(verified_results.items(), start=1):
        print(f"--------------------------------------------------")
        print(f"Prediction {i}: {pred}")
        print(f"    Actual Result: {details['actual']}")
        print(f"    Rating: {details['rating']}\n")
    print(f"#####################################################")

    # Generate and display podcast-style narrative
    print("\n######## Podcast-Style Narrative ########\n")
    narrative = narrative_generator.generate_narrative(video_title=video_title, intro_text=intro_text, verified_results=verified_results)
    print(narrative)

if __name__ == "__main__":
    main()