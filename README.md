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

- **Logging and Monitoring**
  - Comprehensive logging system with multiple levels (INFO, DEBUG, ERROR)
  - Detailed error tracking and debugging information
  - Log file generation with timestamps
  - Configurable verbosity levels

## Installation

### Prerequisites

1. Install FFmpeg (required for audio processing):
   - **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) or install via [Chocolatey](https://chocolatey.org/): `choco install ffmpeg`
   - **macOS**: Install via Homebrew: `brew install ffmpeg`
   - **Linux**: Install via package manager:
     - Ubuntu/Debian: `sudo apt-get install ffmpeg`
     - Fedora: `sudo dnf install ffmpeg`
     - Arch Linux: `sudo pacman -S ffmpeg`

### Python Setup

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

### Command Line Options

- `-?`, `-h`, `--help`: Display help message and command options
- `-t`, `--transcript`: Path to a local transcript text file
- `-u`, `--url`: YouTube video URL to download audio from
- `-v`, `--verbose`: Enable verbose output (sets logging level to INFO)
- `-i`, `--intro-file`: Path to a file with introductory context for the transcript

Example with all options:
```bash
python projectY.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -v -i intros/context.txt
```

### Using Intro Files
You can provide additional context for the analysis using an intro file:
```bash
# Using short form
python projectY.py -u "VIDEO_URL" -i intros/expert_background.txt

# Using long form
python projectY.py -u "VIDEO_URL" --intro-file intros/expert_background.txt
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
│   ├── config.py           # Configuration and environment
│   ├── prompts.py          # AI prompts
│   └── utilities.py        # Utility functions
├── downloads/              # Downloaded audio files (git-ignored)
├── transcripts/           # Generated transcripts (git-ignored)
├── intros/               # Introductory context files (git-ignored)
├── projectY.log          # Application log file (git-ignored)
└── requirements.txt       # Project dependencies
```

## Directory Structure

### downloads/
- Contains downloaded audio files from YouTube videos
- Files are automatically downloaded when processing YouTube URLs
- Format: MP3 files named after the video title
- Note: This directory is git-ignored as it contains downloaded content

### transcripts/
- Contains generated transcripts from audio files
- Created automatically when processing audio or YouTube videos
- Format: Text files named after the source audio/video
- Note: This directory is git-ignored as it contains generated content

### intros/
- Contains introductory context files for transcripts
- Optional files that provide additional context for analysis
- Format: Text files with contextual information
- Note: This directory is git-ignored as it contains user-specific content
- Usage:
  - Files in this directory can be referenced using the `--intro-file` option
  - The content is prepended to the transcript before analysis
  - Useful for providing background information, speaker context, or domain-specific knowledge
  - Example: `--intro-file intros/BruceKasmanIntro.txt` will include Bruce Kasman's background before analyzing his predictions
  - The intro text helps the AI better understand the context and credibility of the predictions

### How Intro Files Work
1. When you specify an intro file using `--intro-file`, the system:
   - Reads the content from the specified file in the `intros/` directory
   - Prepends this content to the transcript before analysis
   - Uses this combined text for prediction extraction and verification
2. This helps the AI by providing:
   - Speaker background and expertise
   - Historical context
   - Domain-specific terminology
   - Previous prediction track record
3. Example intro file content:
   ```
   Bruce Kasman is the Chief Economist at JPMorgan Chase, with over 30 years of experience in economic forecasting. 
   He has a strong track record in predicting economic trends and has been recognized for his accurate forecasts 
   in the financial sector.
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
5. A comprehensive log file (`projectY.log`) with detailed execution information

## Logging

The application uses Python's built-in logging module with the following features:
- Multiple log levels (INFO, DEBUG, ERROR)
- Log file output with timestamps
- Console output for important messages
- Detailed error tracking and debugging information
- Configurable verbosity through command-line options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 and Whisper APIs
- Perplexity AI for prediction verification
- yt-dlp for YouTube video processing
