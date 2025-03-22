from projectY_modules import utilities
import os
import yt_dlp

def download_audio(youtube_url):
    
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)


    try:
        print("Fetching video info...")

        # Step 1: Extract video title before downloading
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)  # Get video info without downloading
            video_title = info_dict.get("title", "audio")  # Get title
            safe_title = utilities.sanitize_filename(video_title)  # Sanitize title
        
        print(f"Using sanitized filename: {safe_title}.mp3")

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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])  # Now downloads directly with sanitized filename

        audio_file_path = output_template.replace("%(ext)s", "mp3")


        print(f"Audio file saved as: {audio_file_path}")

    except Exception as e:
        print(f"Error downloading video: {e}")
        exit(1)

    return audio_file_path