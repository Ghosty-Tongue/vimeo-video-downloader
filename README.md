# Vimeo Video Downloader

This Python script allows you to fetch information about a Vimeo video and download it.

## Prerequisites

- Python 3.x
- Dependencies: `requests`

## Usage

1. Clone the repository:

   ```
   git clone https://github.com/Ghosty-Tongue/vimeo-video-downloader.git
   ```

2. Navigate to the project directory:

   ```
   cd vimeo-video-downloader
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the script:

   ```
   python main.py
   ```

## How it Works

The script takes a Vimeo video ID or URL as input, retrieves information about the video, including resolution, frames per second (FPS), and file size. You can choose to download the video, and the script will create a folder named after the video ID to store the downloaded file.

## File Size Warnings

- If the video file size exceeds 250 MB, a warning will be displayed about potential download time variations based on internet speed.
- If the video file size exceeds 1 GB, a warning will suggest considering a high-speed internet connection.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
