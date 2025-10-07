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
2.  Ensure the following files are all in the same folder:
    - `YouTube_Downloader.exe`
    - `yt-dlp.exe`
    - `ffmpeg.exe`
    - `ffprobe.exe`
3.  Run `YouTube_Downloader.exe`.
4.  Paste the YouTube URL into the input field.
5.  Select the desired video resolution.
6.  Click "Download Video" or "Download Audio (MP3)".
7.  The downloaded file will be saved in the `downloads` folder inside the `dist` directory.

## Dependencies

All required executables (`yt-dlp`, `ffmpeg`) are included in the `vendor` directory and are intended to be distributed alongside the main application executable.

## Building from Source

If you want to build the application from the source code, you will need:

- Python 3
- PyInstaller

```bash
pip install pyinstaller
```

To build the executable, run the following command:

```bash
python -m PyInstaller YouTube_Downloader.spec
```

**Important:** Due to an unresolved issue with PyInstaller, the `datas` directive in the `.spec` file may not work correctly. After the build is complete, you must **manually copy** the contents of the `vendor` folder into the `dist` folder so they are next to the `YouTube_Downloader.exe`.

## License

This project is licensed under the MIT License.
