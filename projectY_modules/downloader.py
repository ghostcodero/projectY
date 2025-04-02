from projectY_modules import utilities
import os
import yt_dlp
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

def download_audio(youtube_url):
    """Download audio from a YouTube URL and save as MP3."""
    logger.info("Fetching video info...")
    logger.debug(f"Processing URL: {youtube_url}")

    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    try:
        # Step 1: Extract video title before downloading
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)  # Get video info without downloading
            video_title = info_dict.get("title", "audio")  # Get title
            safe_title = utilities.sanitize_filename(video_title)  # Sanitize title
        
        logger.debug(f"Original title: {video_title}")
        logger.info(f"Using sanitized filename: {safe_title}.mp3")

        # Step 2: Define yt-dlp options with pre-sanitized filename
        output_template = os.path.join(download_dir, f"{safe_title}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,  # Use sanitized title
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "quiet": True,
            "no_warnings": True
        }

        # Step 3: Download and extract audio with the correct filename
        logger.info("Downloading and converting audio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])  # Now downloads directly with sanitized filename

        audio_file_path = output_template.replace("%(ext)s", "mp3")
        logger.info(f"Audio file saved as: {audio_file_path}")
        logger.debug(f"Full audio path: {os.path.abspath(audio_file_path)}")

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Failed to download video: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while downloading video: {str(e)}", exc_info=True)
        raise

    return audio_file_path