# ProjectY

A tool for analyzing and verifying predictions from YouTube videos or transcripts. ProjectY downloads YouTube videos, transcribes them, extracts predictions, and verifies their outcomes using multiple AI models.

## Features

- **YouTube Video Processing**
  - Download and extract audio from YouTube videos
  - Automatic transcription using OpenAI's Whisper API
  - Support for local transcript files

- **Prediction Analysis**
  - Extract clear, concrete predictions from transcripts
  - Verify predictions using Perplexity AI
  - Rate predictions as TRUE, FALSE, NOT YET, or UNCLEAR

- **Output Generation**
  - Detailed summary of predictions and their outcomes
  - Podcast-style narrative generation
  - Support for introductory context

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ghostcodero/projectY
cd projectY
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up system environment variables:
The following environment variables need to be set in your system:
```
OPENAI_API_KEY=your_openai_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

## Usage

### Basic Usage

Analyze a YouTube video:
```bash
python projectY.py -u "https://www.youtube.com/watch?v=VIDEO_ID"
```

Analyze a local transcript:
```bash
python projectY.py -t path/to/transcript.txt
```

### Advanced Options

- `-v, --verbose`: Enable verbose output
- `--intro-file`: Provide additional context for the transcript

Example with all options:
```bash
python projectY.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -v --intro-file context.txt
```

## Project Structure

```
projectY/
├── projectY.py              # Main script
├── projectY_modules/        # Core functionality modules
│   ├── downloader.py       # YouTube video download
│   ├── transcriber.py      # Audio transcription
│   ├── prediction_extractor.py  # Prediction extraction
│   ├── prediction_verifier.py   # Prediction verification
│   ├── narrative_generator.py   # Narrative generation
│   ├── prompts.py          # AI prompts
│   └── utilities.py        # Utility functions
├── downloads/              # Downloaded audio files
├── transcripts/           # Generated transcripts
└── requirements.txt       # Project dependencies
```

## Dependencies

- Python 3.9+
- openai
- yt-dlp
- requests

## Environment Variables

The following system environment variables must be set:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)

## Output

The tool generates:
1. A detailed list of predictions with their verification status
2. A podcast-style narrative summarizing the analysis
3. Saved transcripts in the `transcripts/` directory
4. Downloaded audio files in the `downloads/` directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 and Whisper APIs
- Perplexity AI for prediction verification
- yt-dlp for YouTube video processing
