# YouTube Downloader

A simple GUI application to download YouTube videos and audio.

## Features

-   Download YouTube videos in different resolutions (1080p, 720p, 480p).
-   Download audio only and save it as an MP3 file.
-   User-friendly graphical interface.
-   Displays download progress.
-   Saves files to a `downloads` folder.

## Requirements

-   Python 3
-   [yt-dlp](https://github.com/yt-dlp/yt-dlp)
-   [FFmpeg](https://ffmpeg.org/download.html) (must be installed and in the system's PATH)

You can install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1.  Run the `youtube_downloader.py` script:

    ```bash
    python youtube_downloader.py
    ```

2.  Paste the YouTube URL into the input field.
3.  Select the desired video resolution.
4.  Click "Download Video" or "Download Audio (MP3)".
5.  The downloaded file will be saved in the `downloads` folder.

## License

This project is licensed under the MIT License.