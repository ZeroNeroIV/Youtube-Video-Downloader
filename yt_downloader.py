import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import time

# Global variables for process control
current_process = None
is_cancelled = False
download_thread = None

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)

def start_download_thread():
    global download_thread, is_cancelled
    
    if download_thread and download_thread.is_alive():
        messagebox.showinfo("Busy", "Download is already in progress.")
        return

    # Reset state
    is_cancelled = False
    
    # UI updates (Disable Download, Enable Cancel)
    btn_download.config(state="disabled")
    btn_cancel.config(state="normal")
    status_var.set("Starting download...")
    
    # Start thread
    download_thread = threading.Thread(target=download_video_logic)
    download_thread.daemon = True
    download_thread.start()

def cancel_download():
    global is_cancelled, current_process
    
    if not (download_thread and download_thread.is_alive()):
        return

    if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
        is_cancelled = True
        status_var.set("Cancelling...")
        
        # Kill the subprocess if running
        if current_process:
            try:
                current_process.terminate() # Using terminate to be nicer, kill() if stubborn
                # On Windows terminate() is effectively kill()
            except Exception:
                pass

def download_video_logic():
    global current_process
    
    urls_text = url_text.get("1.0", tk.END).strip()
    urls = [line.strip() for line in urls_text.split('\n') if line.strip()]
    output_path = output_path_var.get().strip()
    base_filename = filename_var.get().strip()
    
    if not urls:
        messagebox.showerror("Error", "Please enter at least one YouTube video URL.")
        reset_ui()
        return
    if not output_path:
        messagebox.showerror("Error", "Please choose an output path.")
        reset_ui()
        return

    # No filename check - it's optional now

    try:
        os.makedirs(output_path, exist_ok=True)
        
        success_count = 0
        error_messages = []

        format_choice = format_var.get()
        is_playlist = playlist_var.get()

        for index, url in enumerate(urls):
            if is_cancelled:
                break
            
            status_var.set(f"Downloading {index+1}/{len(urls)}: ...")
            
            try:
                # determine filename for this specific item
                if base_filename:
                    # If multiple files, append index to avoid overwrite, unless it's just one file
                    if len(urls) > 1:
                        # User requested index then name: "1_CustomName"
                        final_filename = f"{index+1}_{base_filename}"
                    else:
                        final_filename = base_filename
                    
                    # Append extension
                    ext = ".mp3" if format_choice == "mp3" else ".mp4"
                    if not final_filename.endswith(ext):
                        final_filename += ext
                    
                    full_path = os.path.join(output_path, final_filename)
                    template_arg = full_path # Explicit path
                else:
                    # Let yt-dlp name it based on title, but we want the index prefix.
                    # Case A: Playlist Mode
                    if is_playlist:
                        # Use playlist index
                        # Structure: playlist_folder/index_title.ext
                        name_template = "%(playlist_index)s_%(title)s.%(ext)s"
                    else:
                        # Case B: Batch Mode (Single videos)
                        # Structure: playlist_folder(optional)/batch_index_title.ext
                        name_template = f"{index+1}_%(title)s.%(ext)s"

                    # Apply subfolder logic
                    template_arg = os.path.join(output_path, "%(playlist_title&{}/|)s" + name_template)

                # Build yt-dlp command
                command = ["yt-dlp", "-o", template_arg, url]
                
                # Playlist toggle
                if is_playlist:
                    command.append("--yes-playlist")
                else:
                    command.append("--no-playlist")

                if format_choice == "mp3":
                    command.extend(["-x", "--audio-format", "mp3"])
                else:
                    command.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])
                
                # Run download with Popen to allow cancellation
                # Creationflags=0x08000000 (CREATE_NO_WINDOW) to hide console window if we wanted, 
                # but maybe useful to see it? User didn't ask to hide it.
                # However, communicating wait is needed.
                current_process = subprocess.Popen(command)
                exit_code = current_process.wait()
                current_process = None

                if is_cancelled:
                    break

                if exit_code == 0:
                    success_count += 1
                else:
                    error_messages.append(f"Failed {url}: Exit code {exit_code}")
            
            except Exception as e:
                error_messages.append(f"Error with {url}: {e}")

        # Summary
        if is_cancelled:
            status_var.set("Download cancelled.")
            messagebox.showinfo("Cancelled", "Download operation was cancelled.")
        elif not error_messages:
            status_var.set("Complete!")
            messagebox.showinfo("Success", f"All {success_count} files downloaded successfully!")
        else:
            status_var.set("Completed with errors.")
            msg = f"Downloaded {success_count}/{len(urls)} files.\n\nErrors:\n" + "\n".join(error_messages)
            messagebox.showwarning("Partial Success", msg)

    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("System Error", str(e))
    finally:
        reset_ui()

def reset_ui():
    global current_process
    current_process = None
    btn_download.config(state="normal")
    btn_cancel.config(state="disabled")
    if not status_var.get().startswith("Complete") and not status_var.get().startswith("Download cancelled"):
         status_var.set("Ready")


# === GUI Setup ===
root = tk.Tk()
root.title("YouTube Video Downloader (yt-dlp)")
root.geometry("600x350")

# Variables
# url_var removed, using Text widget
output_path_var = tk.StringVar()
filename_var = tk.StringVar()
format_var = tk.StringVar(value="mp4")
playlist_var = tk.BooleanVar(value=False)
status_var = tk.StringVar(value="Ready")

# URL Input (Text Area)
tk.Label(root, text="YouTube Video URLs (one per line):").grid(row=0, column=0, sticky="ne", padx=5, pady=5)
url_text = tk.Text(root, height=5, width=50)
url_text.grid(row=0, column=1, padx=5, pady=5)
# Scrollbar for text area
scrollbar = tk.Scrollbar(root, command=url_text.yview)
scrollbar.grid(row=0, column=2, sticky='ns')
url_text['yscrollcommand'] = scrollbar.set

# Output Path Input
tk.Label(root, text="Output Path:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=output_path_var, width=40).grid(row=1, column=1, sticky="w", padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=5, pady=5, sticky='w')

# Format Selection
tk.Label(root, text="Format:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
frame_format = tk.Frame(root)
frame_format.grid(row=2, column=1, sticky="w", padx=5, pady=5)
tk.Radiobutton(frame_format, text="Video (MP4)", variable=format_var, value="mp4").pack(side="left", padx=5)
tk.Radiobutton(frame_format, text="Audio (MP3)", variable=format_var, value="mp3").pack(side="left", padx=5)
tk.Checkbutton(root, text="Download Playlist (if detected)", variable=playlist_var).grid(row=2, column=2, sticky='w', padx=5)

# Filename Input
# Filename Input
tk.Label(root, text="Filename (Optional):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=filename_var, width=50).grid(row=3, column=1, padx=5, pady=5)
tk.Label(root, text="(Leave empty to use video title)").grid(row=3, column=2, sticky="w", padx=2)

# Download Button & Cancel
frame_actions = tk.Frame(root)
frame_actions.grid(row=4, column=1, pady=15)

btn_download = tk.Button(frame_actions, text="Download All", command=start_download_thread, bg="green", fg="white", width=15)
btn_download.pack(side="left", padx=10)

btn_cancel = tk.Button(frame_actions, text="Cancel", command=cancel_download, bg="red", fg="white", state="disabled", width=15)
btn_cancel.pack(side="left", padx=10)

# Status Label
tk.Label(root, textvariable=status_var, fg="blue").grid(row=5, column=0, columnspan=3, pady=5)

# Run App
root.mainloop()
