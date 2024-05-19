import os
import re
import requests
from tqdm import tqdm

def sanitize_filename(filename):
    """Remove any invalid characters from the filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_video(video_url, video_title, file_extension):
    try:
        sanitized_title = sanitize_filename(video_title)
        file_name = f"{sanitized_title}.{file_extension}"
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        with open(file_name, 'wb') as file, tqdm(
            desc=file_name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
        print(f"\nVideo saved as: {file_name}")
    except requests.RequestException as e:
        print(f"Failed to download video. Error: {e}")

def get_vimeo_video_info(video_id):
    vimeo_config_url = f"https://player.vimeo.com/video/{video_id}/config"
    try:
        response = requests.get(vimeo_config_url)
        response.raise_for_status()
        config_data = response.json()

        video_title = config_data.get("video", {}).get("title")
        if not video_title:
            return "Failed to retrieve video title.", None, None

        files = config_data.get("request", {}).get("files", {})

        # Check for MP4 format
        if "progressive" in files:
            # Progressive option (MP4)
            progressive_files = files["progressive"]
            best_quality = max(progressive_files, key=lambda x: x['width'])
            video_url = best_quality["url"]
            file_extension = "mp4"
            return video_url, video_title, file_extension
        else:
            # Check for HLS or DASH formats
            if "hls" in files or "dash" in files:
                return "This video is available only in HLS or DASH format, which cannot be downloaded as an MP4.", None, None
            else:
                return "No downloadable video file found in the player config.", None, None
    except requests.RequestException as e:
        return f"Failed to fetch player config. Error: {e}", None, None

if __name__ == "__main__":
    video_id = input("Enter the Vimeo video ID: ")
    video_info = get_vimeo_video_info(video_id)

    if isinstance(video_info, tuple):
        video_url, video_title, file_extension = video_info
        if video_url and video_title:
            print(f"Video Information:\nURL: {video_url}\nTitle: {video_title}")
            download_video(video_url, video_title, file_extension)
        else:
            print(f"Error: {video_title}")
    else:
        print(video_info)
