# YouTube Downloader

A simple GUI application to download YouTube videos and audio, designed to be portable and easy to use.

## Features

- Download YouTube videos in different resolutions (1080p, 720p, 480p).
- Download audio only and save it as an MP3 file.
- User-friendly graphical interface.
- Displays real-time download progress and detailed logs.
- Fully portable: no installation of Python, yt-dlp, or FFmpeg required.
- Saves files to a `downloads` folder.

## Installation and Usage

This application is designed to be run as a standalone executable without any installation.

1.  Go to the `dist` directory.
2.  Run `YouTube_Downloader.exe`.
3.  Paste the YouTube URL into the input field.
4.  Select the desired video resolution.
5.  Click "Download Video" or "Download Audio (MP3)".
6.  The downloaded file will be saved in the `downloads` folder.

## Dependencies

All required executables (`yt-dlp`, `ffmpeg`) are included in the `vendor` directory and are automatically packaged with the application during the build process.

## Building from Source

If you want to build the application from the source code, you will need:

- Python 3
- PyInstaller

```bash
pip install pyinstaller
```

To build the executable, run the following command from the project root directory:

```bash
pyinstaller YouTube_Downloader.spec
```

This will create a `dist` folder containing the final `YouTube_Downloader.exe` and all its necessary dependencies.

## License

This project is licensed under the MIT License.