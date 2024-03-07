import os
import requests
import time
from tqdm import tqdm

def get_video_info(video_url):
    response = requests.head(video_url)
    if response.status_code == 200:
        size = int(response.headers.get("Content-Length", 0))
        size_readable = convert_bytes_to_human_readable(size)
        return size_readable
    else:
        return f"Failed to fetch video information. Status code: {response.status_code}"

def download_video(video_url, video_title):
    video_response = requests.get(video_url, stream=True)
    if video_response.status_code == 200:
        file_size = int(video_response.headers.get("Content-Length", 0))
        file_size_readable = convert_bytes_to_human_readable(file_size)

        print(f"Downloading video '{video_title}'...")
        start_time = time.time()

        file_extension = "mp4"  # Assuming the video is in mp4 format
        file_name = f"{video_title}.{file_extension}"

        with open(file_name, 'wb') as file:
            with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for chunk in video_response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

        elapsed_time = time.time() - start_time
        elapsed_time_readable = convert_seconds_to_human_readable(elapsed_time)

        print(f"\nDownload completed. File size: {file_size_readable}.")
        print(f"Elapsed time: {elapsed_time_readable}")
        print(f"Video saved as: {file_name}")

    else:
        print(f"Failed to download video. Status code: {video_response.status_code}")

def get_vimeo_video_info(video_id):
    vimeo_config_url = f"https://player.vimeo.com/video/{video_id}/config"
    response = requests.get(vimeo_config_url)

    if response.status_code == 200:
        config_data = response.json()

        if "video" in config_data and "title" in config_data["video"]:
            video_title = config_data["video"]["title"]
        else:
            video_title = "Untitled"

        if "request" in config_data and "files" in config_data["request"] and "progressive" in config_data["request"]["files"]:
            progressive_files = config_data["request"]["files"]["progressive"]
            if progressive_files:
                highest_quality_file = max(progressive_files, key=lambda x: x["height"])
                video_url = highest_quality_file["url"]
                return video_url, video_title
            else:
                return "No progressive video file found in the player config", None
        else:
            return "Invalid player config data", None
    else:
        return f"Failed to fetch player config. Status code: {response.status_code}", None

def convert_bytes_to_human_readable(size_in_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0

    while size_in_bytes >= 1024 and index < len(units) - 1:
        size_in_bytes /= 1024.0
        index += 1

    return f"{size_in_bytes:.2f} {units[index]}"

def convert_seconds_to_human_readable(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

if __name__ == "__main__":
    video_id = input("Enter the Vimeo video ID: ")
    video_info = get_vimeo_video_info(video_id)

    if isinstance(video_info, tuple):
        video_url, video_title = video_info
        print(f"Video Information:\nURL: {video_url}\nTitle: {video_title}")
        download_video(video_url, video_title)
    else:
        print(video_info)
