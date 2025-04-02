from projectY_modules import config
from projectY_modules import downloader 
from projectY_modules import transcriber
from projectY_modules import prediction_extractor
from projectY_modules import prediction_verifier
from projectY_modules import narrative_generator

import argparse
import sys
import os
import logging

def setup_logging(verbose):
    """Configure logging based on verbosity level."""
    level = logging.INFO if verbose else logging.WARNING
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configure file handler for debug log with append mode
    file_handler = logging.FileHandler('projectY.log', mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # Always log debug to file

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def parse_args():
    parser = argparse.ArgumentParser(description="Verify predictions from YouTube or transcript.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--transcript", help="Path to a local transcript text file")
    group.add_argument("-u", "--url", help="YouTube video URL to download audio from")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--intro-file", type=str, help="Optional path to a file with introductory context for the transcript.")
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    sys.stdout.reconfigure(encoding='utf-8')
    intro_text = ""
    video_title = "Unknown Video"

    try:
        if args.transcript:
            with open(args.transcript, "r", encoding="utf-8") as f:
                transcribed_text = f.read()
            logger.info(f"Loaded transcript from: {args.transcript}")
            video_title = os.path.splitext(os.path.basename(args.transcript))[0]

        elif args.url:
            logger.info(f"Downloading audio from: {args.url}")
            audio_file = downloader.download_audio(args.url)
            transcribed_text = transcriber.transcribe_audio(audio_file)
            video_title = os.path.splitext(os.path.basename(audio_file))[0]

        else:
            url = input("Enter the YouTube video URL: ")
            logger.info(f"Downloading audio from: {url}")
            audio_file = downloader.download_audio(url)
            transcribed_text = transcriber.transcribe_audio(audio_file)
            video_title = os.path.splitext(os.path.basename(audio_file))[0]

        if args.intro_file:
            if os.path.exists(args.intro_file):
                with open(args.intro_file, "r", encoding="utf-8") as f:
                    intro_text = f.read().strip()
                logger.info(f"Loaded intro from: {args.intro_file}")
            else:
                logger.warning(f"Intro file not found: {args.intro_file}")

        prediction_list = prediction_extractor.extract_predictions(
            transcribed_text, 
            intro=intro_text
        )
        
        verified_results = {}
        for prediction in prediction_list:
            logger.info(f"\nAnalyzing prediction: {prediction}")
            logger.info("Asking Perplexity to verify...")

            gpt_response = prediction_verifier.verify_prediction_with_perplexity(prediction)
            
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

        # Print final results (keeping these as prints for clear output formatting)
        print("\n" + "="*50)
        print("Final Verified Predictions")
        print("="*50 + "\n")
        
        for i, (pred, details) in enumerate(verified_results.items(), start=1):
            print(f"Prediction {i}: {pred}")
            print(f"    Actual Result: {details['actual']}")
            print(f"    Rating: {details['rating']}\n")
        
        print("="*50)

        # Generate and display podcast-style narrative
        print("\nPodcast-Style Narrative\n" + "="*50)
        narrative = narrative_generator.generate_narrative(
            video_title=video_title,
            intro_text=intro_text,
            verified_results=verified_results
        )
        print(narrative)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()