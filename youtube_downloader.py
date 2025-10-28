import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import queue
import subprocess
import re
import sys

# Determine the base path for resources, works for both script and bundled exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Queue for logging messages from download thread to GUI thread
log_queue = queue.Queue()

def process_log_queue():
    """Processes messages from the log_queue and updates the Text widget."""
    try:
        while True:
            message = log_queue.get_nowait()
            log_text.config(state="normal")
            log_text.insert(tk.END, message + "\n")
            log_text.see(tk.END) # Scroll to the end
            log_text.config(state="disabled")
    except queue.Empty:
        pass
    finally:
        root.after(100, process_log_queue) # Check again after 100ms

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
    resolution_var = tk.StringVar(value="720")
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

    # Log display
    global log_text
    log_frame = ttk.LabelFrame(main_frame, text="Log")
    log_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)

    log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical")
    log_scrollbar.grid(row=0, column=1, sticky="ns")

    log_text = tk.Text(log_frame, height=10, wrap="word", yscrollcommand=log_scrollbar.set)
    log_text.grid(row=0, column=0, sticky="nsew")
    log_text.config(state="disabled")

    log_scrollbar.config(command=log_text.yview)

    # Footer Label
    footer_label = ttk.Label(main_frame, text="류용효컨셉맵연구소", anchor="center")
    footer_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    main_frame.grid_rowconfigure(5, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

def get_download_path():
    # Save downloads to a 'downloads' folder in the application's directory
    download_dir = os.path.join(application_path, "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

def start_video_download_thread():
    threading.Thread(target=download_video, daemon=True).start()

def start_audio_download_thread():
    threading.Thread(target=download_audio, daemon=True).start()

def clear_log():
    log_text.config(state="normal")
    log_text.delete(1.0, tk.END)
    log_text.config(state="disabled")

def run_command(command, cwd=None):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW, cwd=cwd)

        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue
            
            log_queue.put(line)

            if '[download]' in line and '%' in line:
                match = re.search(r'(\d+\.\d+)%', line)
                if match:
                    percentage = float(match.group(1))
                    progress_bar['value'] = percentage
                    status_label.config(text=f"Status: Downloading... {percentage:.1f}%")
                    root.update_idletasks()
        
        process.wait()
        return process.returncode
    except FileNotFoundError:
        log_queue.put(f"ERROR: Cannot find {command[0]}. Make sure yt-dlp.exe and ffmpeg.exe are in the same folder as the application.")
        return -1
    except Exception as e:
        log_queue.put(f"ERROR: An unexpected error occurred: {e}")
        return -1

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    clear_log()
    status_label.config(text="Status: Preparing to download...")
    progress_bar['value'] = 0
    root.update_idletasks()

    yt_dlp_path = os.path.join(application_path, "yt-dlp.exe")
    vendor_dir = os.path.dirname(yt_dlp_path)
    yt_dlp_executable = os.path.basename(yt_dlp_path)
    download_path = get_download_path()
    resolution = resolution_var.get()

    command = [
        yt_dlp_executable,
        '--ffmpeg-location', vendor_dir,
        '--progress',
        '--verbose',
        '--encoding', 'utf-8',
        '-f', f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[height<={resolution}][ext=mp4]/best',
        '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
        url
    ]

    return_code = run_command(command, cwd=vendor_dir)

    if return_code == 0:
        status_label.config(text="Status: Download Complete!")
        messagebox.showinfo("Success", "Video downloaded successfully!")
    else:
        status_label.config(text="Status: Error")
        messagebox.showerror("Error", "An error occurred. Check the log for details.")
    
    progress_bar['value'] = 0

def download_audio():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    clear_log()
    status_label.config(text="Status: Preparing to download...")
    progress_bar['value'] = 0
    root.update_idletasks()

    yt_dlp_path = os.path.join(application_path, "yt-dlp.exe")
    vendor_dir = os.path.dirname(yt_dlp_path)
    yt_dlp_executable = os.path.basename(yt_dlp_path)
    download_path = get_download_path()

    command = [
        yt_dlp_executable,
        '--ffmpeg-location', vendor_dir,
        '--progress',
        '--encoding', 'utf-8',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '320K',
        '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
        url
    ]

    return_code = run_command(command, cwd=vendor_dir)

    if return_code == 0:
        status_label.config(text="Status: Download Complete!")
        messagebox.showinfo("Success", "Audio downloaded successfully as MP3!")
    else:
        status_label.config(text="Status: Error")
        messagebox.showerror("Error", "An error occurred. Check the log for details.")

    progress_bar['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    root.title("YouTube Downloader (yt-dlp)")
    root.geometry("500x450")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)

    create_widgets()

    process_log_queue()

    root.mainloop()
