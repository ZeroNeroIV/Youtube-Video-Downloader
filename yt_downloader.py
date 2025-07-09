import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)

def download_video():
    url = url_var.get().strip()
    output_path = output_path_var.get().strip()
    filename = filename_var.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return
    if not output_path:
        messagebox.showerror("Error", "Please choose an output path.")
        return
    if not filename:
        messagebox.showerror("Error", "Please enter a filename.")
        return

    try:
        os.makedirs(output_path, exist_ok=True)
        full_path = os.path.join(output_path, filename)

        # Add .mp4 if not included
        if not full_path.endswith(".mp4"):
            full_path += ".mp4"
        
        # Run yt-dlp download command
        command = ["yt-dlp", "-f", "best[ext=mp4]", "-o", full_path, url]
        subprocess.run(command, check=True)

        messagebox.showinfo("Success", f"Downloaded to: {full_path}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Download Failed", str(e))


# === GUI Setup ===
root = tk.Tk()
root.title("YouTube Video Downloader (yt-dlp)")
root.geometry("600x200")

# Variables
url_var = tk.StringVar()
output_path_var = tk.StringVar()
filename_var = tk.StringVar()

# URL Input
tk.Label(root, text="YouTube Video URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=url_var, width=50).grid(row=0, column=1, padx=5, pady=5)

# Output Path Input
tk.Label(root, text="Output Path:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=output_path_var, width=40).grid(row=1, column=1, sticky="w", padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=5, pady=5)

# Filename Input
tk.Label(root, text="Video Filename:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=filename_var, width=50).grid(row=2, column=1, padx=5, pady=5)

# Download Button
tk.Button(root, text="Download", command=download_video, bg="green", fg="white").grid(row=3, column=1, pady=15)

# Run App
root.mainloop()
