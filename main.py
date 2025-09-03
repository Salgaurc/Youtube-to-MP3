import yt_dlp
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk  # Import Pillow for handling icns
import sys
import os

# Function to get the path to the icon
def resource_path(relative_path):
    """Get the absolute path to the resource, works for both dev and bundled"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to handle downloading
def download_mp3(url, download_path, status_var, progress_var):
    def hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip()
            progress_var.set(percent)
            status_var.set("Downloading...")
            progress_bar.grid()  # Make it visible during the download
        elif d['status'] == 'finished':
            progress_var.set("100%")
            status_var.set("Converting to MP3...")
            progress_bar.grid_remove()  # Hide it when done

    # Specify the path to ffmpeg
    ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # Path to your ffmpeg

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title).200s.%(ext)s',  # Trim long/unsafe filenames
        'ffmpeg_location': ffmpeg_path,  # Specify the ffmpeg location
        'progress_hooks': [hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noprogress': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_var.set("✅ Download complete!")
    except PermissionError:
        status_var.set("❌ Write permission error")
        progress_var.set("")
        messagebox.showerror("Permission Error", "You don't have permission to write to that folder.")
    except Exception as e:
        status_var.set("❌ Error")
        progress_var.set("")
        messagebox.showerror("Download Failed", str(e))

# Triggered by download button
def on_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Required", "Please paste a YouTube URL.")
        return

    folder = filedialog.askdirectory(title="Select Save Location")
    if not folder:
        return

    threading.Thread(
        target=download_mp3,
        args=(url, folder, status_var, progress_var),
        daemon=True
    ).start()

# Initialize app window
app = tk.Tk()
app.title("YouTube → MP3 Converter")
app.geometry("500x280")
app.resizable(False, False)
app.configure(bg="#1e1e1e")

# Load the icon and set it for the window (using Pillow to handle .icns)
icon_path = resource_path("icon.icns")  # Get the correct path
try:
    icon_image = Image.open(icon_path)  # Load the .icns file
    icon = ImageTk.PhotoImage(icon_image)  # Convert it to PhotoImage for Tkinter
    app.tk.call('wm', 'iconphoto', app._w, icon)  # Set the window icon
except Exception as e:
    print(f"Error loading icon: {e}")

# Styling
style = ttk.Style(app)
style.theme_use('clam')
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TButton", background="#0a84ff", foreground="white", padding=6)
style.configure("TFrame", background="#1e1e1e")
style.configure("TProgressbar", troughcolor="#2c2c2e", background="#0a84ff", thickness=20, relief="flat")

# Style Entry widget (theme limitation workaround)
url_entry_style = ttk.Style()
url_entry_style.configure("TEntry", fieldbackground="#2c2c2e", foreground="white")

# Layout
main_frame = ttk.Frame(app, padding=20, style="TFrame")
main_frame.columnconfigure(0, weight=1)
main_frame.pack(expand=True, padx=20, pady=20)

status_var = tk.StringVar(value="")
progress_var = tk.StringVar(value="")

# Progress bar + label (top)
progress_bar = ttk.Progressbar(main_frame, mode='determinate', maximum=100)
progress_bar.grid(row=0, column=0, pady=(0, 5), sticky="ew")
progress_bar.grid_remove()  # Hide the progress bar initially

progress_label = ttk.Label(main_frame, textvariable=progress_var)
progress_label.grid(row=1, column=0, sticky="w")

# URL input
ttk.Label(main_frame, text="YouTube URL:").grid(row=2, column=0, sticky="w", pady=(10, 5))
url_entry = ttk.Entry(main_frame, width=55, style="TEntry")
url_entry.grid(row=3, column=0, pady=(0, 15), sticky="ew")

# Button (shorter width)
download_btn = ttk.Button(main_frame, text="Download MP3", command=on_download)
download_btn.grid(row=4, column=0, pady=(0, 15))  # Removed sticky="ew" to keep it short

# Status label
status_label = ttk.Label(main_frame, textvariable=status_var)
status_label.grid(row=5, column=0, pady=(10, 0), sticky="w")

# Progress bar updater
def update_progress_bar():
    try:
        percent = float(progress_var.get().replace('%', ''))
        progress_bar['value'] = percent
    except ValueError:
        progress_bar['value'] = 0
    app.after(500, update_progress_bar)

update_progress_bar()
app.mainloop()