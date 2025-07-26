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

        # Try different approaches for audio download
        ydl_opts_list = [
            # Option 1: Try to download MP3 directly (if available)
            {
                'format': 'bestaudio[ext=mp3]/bestaudio',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                "quiet": True,
                "no_warnings": True
            },
            # Option 2: Download best audio and convert (requires FFmpeg)
            {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                "quiet": True,
                "no_warnings": True
            },
            # Option 3: Download audio without conversion (no FFmpeg needed)
            {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
                'outtmpl': output_template,
                "quiet": True,
                "no_warnings": True
            }
        ]

        # Try each option until one works
        for i, ydl_opts in enumerate(ydl_opts_list):
            try:
                logger.info(f"Trying download option {i+1}...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])
                
                # Check what file was actually downloaded
                if i < 2:  # Options 1 and 2 should create MP3
                    audio_file_path = output_template.replace("%(ext)s", "mp3")
                else:  # Option 3 creates original format
                    # Find the actual downloaded file
                    for ext in ['m4a', 'webm', 'mp3', 'mp4']:
                        test_path = output_template.replace("%(ext)s", ext)
                        if os.path.exists(test_path):
                            audio_file_path = test_path
                            break
                    else:
                        # If no file found, try to find any audio file in downloads
                        for file in os.listdir(download_dir):
                            if file.startswith(safe_title) and any(file.endswith(ext) for ext in ['.m4a', '.webm', '.mp3', '.mp4']):
                                audio_file_path = os.path.join(download_dir, file)
                                break
                        else:
                            raise FileNotFoundError("No audio file found after download")
                
                logger.info(f"Audio file saved as: {audio_file_path}")
                logger.debug(f"Full audio path: {os.path.abspath(audio_file_path)}")
                return audio_file_path
                
            except Exception as e:
                logger.warning(f"Download option {i+1} failed: {str(e)}")
                if i == len(ydl_opts_list) - 1:  # Last option
                    raise
                continue

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Failed to download video: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while downloading video: {str(e)}", exc_info=True)
        raise

    return audio_file_path