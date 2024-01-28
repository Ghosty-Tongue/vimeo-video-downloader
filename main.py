import os
import requests
import time
from urllib.parse import urlparse, parse_qs

def get_video_id(input_str):
    
    parsed_url = urlparse(input_str)
    query_params = parse_qs(parsed_url.query)
    
    if parsed_url.hostname == "vimeo.com" and query_params.get("clip_id"):
        return query_params["clip_id"][0]
    else:
        return input_str 

def get_video_info(video_url):
    
    response = requests.head(video_url)
    
    if response.status_code == 200:
        size = int(response.headers.get("Content-Length", 0))
        size_readable = convert_bytes_to_human_readable(size)
        check_file_size_warning(size)

        return size_readable
    else:
        return f"Failed to fetch video information. Status code: {response.status_code}"

def download_video(video_url, video_id):
    
    folder_name = f"video_{video_id}"
    os.makedirs(folder_name, exist_ok=True)

    video_response = requests.get(video_url, stream=True)
    
    if video_response.status_code == 200:
        file_size = int(video_response.headers.get("Content-Length", 0))
        file_size_readable = convert_bytes_to_human_readable(file_size)
        
        print(f"Downloading video to '{folder_name}'...")
        start_time = time.time()

        with open(os.path.join(folder_name, f"video_{video_id}.mp4"), 'wb') as file:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        elapsed_time = time.time() - start_time
        elapsed_time_readable = convert_seconds_to_human_readable(elapsed_time)

        print(f"Download completed. File size: {file_size_readable}.")
        print(f"Elapsed time: {elapsed_time_readable}")

    else:
        print(f"Failed to download video. Status code: {video_response.status_code}")

def get_vimeo_video_info(video_id):
    
    vimeo_config_url = f"https://player.vimeo.com/video/{video_id}/config"
    response = requests.get(vimeo_config_url)
    
    if response.status_code == 200:
        config_data = response.json()
        
        if "files" in config_data["request"]:
            progressive_files = config_data["request"]["files"]["progressive"]
            
            if progressive_files:
                highest_quality_file = max(progressive_files, key=lambda x: x["height"])
                video_url = highest_quality_file["url"]
                resolution = f"{highest_quality_file['width']}x{highest_quality_file['height']}"
                fps = highest_quality_file["fps"]

                video_size = get_video_info(video_url)
                check_file_size_warning(int(float(video_size.split()[0])))

                return video_url, resolution, fps, video_size
            else:
                return "No video file link found in the player config"
        else:
            return "No 'files' key in the player congfig."
    else:
        return f"Failed to fetch player config. Status code: {response.status_code}"

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

def check_file_size_warning(size):
    
    if size > 250000000:  # 250 MB
        print("Warning: The video file size exceeds 250 MB. Download time may vary based on your internet speed.")
    elif size > 1000000000:  # 1 GB
        print("Warning: The video file size exceeds 1 GB. Consider a high-speed internet connection.")

if __name__ == "__main__":
    user_input = input("Enter Vimeo video ID or URL: ")
    video_id = get_video_id(user_input)

    if video_id:
        video_info = get_vimeo_video_info(video_id)

        if isinstance(video_info, tuple):
            print(f"Video Information:\nURL: {video_info[0]}\nResolution: {video_info[1]}\nFPS: {video_info[2]}\nSize: {video_info[3]}")
            
            download_option = input("Do you want to download the video? (yes/no): ").lower()

            if download_option == "yes":
                download_video(video_info[0], video_id)
        else:
            print(video_info)
    else:
        print("Invalid Vimeo video ID")
