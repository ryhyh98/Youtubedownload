import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading

def create_widgets():
    # URL Input
    url_label = ttk.Label(main_frame, text="YouTube URL:")
    url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    global url_entry
    url_entry = ttk.Entry(main_frame, width=60)
    url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

    # Resolution Selection
    resolution_label = ttk.Label(main_frame, text="Resolution:")
    resolution_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    global resolution_var
    resolution_var = tk.StringVar(value="720") # Value is now just the number
    resolutions = [("1080p", "1080"), ("720p", "720"), ("480p", "480")]
    for i, (text, val) in enumerate(resolutions):
        rb = ttk.Radiobutton(main_frame, text=text, variable=resolution_var, value=val)
        rb.grid(row=1, column=i+1, padx=5, pady=5, sticky="w")

    # Download Buttons
    video_button = ttk.Button(main_frame, text="Download Video", command=start_video_download_thread)
    video_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    audio_button = ttk.Button(main_frame, text="Download Audio (MP3)", command=start_audio_download_thread)
    audio_button.grid(row=2, column=2, padx=5, pady=10, sticky="ew")

    # Status Label
    global status_label
    status_label = ttk.Label(main_frame, text="Status: Ready", anchor="w")
    status_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    # Progress Bar
    global progress_bar
    progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    # Footer Label
    footer_label = ttk.Label(main_frame, text="류용효컨셉맵연구소", anchor="center")
    footer_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")


def get_download_path():
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total_bytes:
            percentage = (d['downloaded_bytes'] / total_bytes) * 100
            progress_bar['value'] = percentage
            status_label.config(text=f"Status: Downloading... {percentage:.1f}%")
            root.update_idletasks()
    elif d['status'] == 'finished':
        status_label.config(text="Status: Download finished, now processing...")
        progress_bar['value'] = 100
        root.update_idletasks()

def start_video_download_thread():
    threading.Thread(target=download_video).start()

def start_audio_download_thread():
    threading.Thread(target=download_audio).start()

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        status_label.config(text="Status: Preparing to download...")
        progress_bar['value'] = 0
        root.update_idletasks()

        download_path = get_download_path()
        resolution = resolution_var.get()

        ydl_opts = {
            'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[height<={resolution}][ext=mp4]/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            status_label.config(text=f"Status: Downloading '{title}'...")
            ydl.download([url])

        status_label.config(text="Status: Download Complete!")
        messagebox.showinfo("Success", f"Video '{title}' downloaded successfully!")
        progress_bar['value'] = 0

    except Exception as e:
        # Check for ffmpeg error
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
             messagebox.showerror("Error", "FFmpeg not found! Please install FFmpeg and add it to your system's PATH.")
        else:
            messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Status: Error")
        progress_bar['value'] = 0

def download_audio():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        status_label.config(text="Status: Preparing to download...")
        progress_bar['value'] = 0
        root.update_idletasks()

        download_path = get_download_path()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'audio')
            status_label.config(text=f"Status: Downloading audio for '{title}'...")
            ydl.download([url])

        status_label.config(text="Status: Download Complete!")
        messagebox.showinfo("Success", f"Audio '{title}' downloaded successfully as MP3!")
        progress_bar['value'] = 0

    except Exception as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
             messagebox.showerror("Error", "FFmpeg not found! Please install FFmpeg and add it to your system's PATH.")
        else:
            messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Status: Error")
        progress_bar['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    root.title("YouTube Downloader (yt-dlp)")
    root.geometry("500x230")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)

    create_widgets()

    root.mainloop()