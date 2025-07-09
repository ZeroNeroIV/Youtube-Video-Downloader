# YouTube Video Downloader (yt-dlp GUI)

A simple desktop application to download YouTube videos using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp). This tool features a lightweight GUI built with Tkinter, allowing users to input a video URL, choose a destination folder, and specify a custom filename for fast and flexible downloads.

## 🎯 Features

- 📺 Download videos in the best available `.mp4` quality
- 🖱️ Simple, user-friendly interface (no command line needed)
- 📁 Custom output folder selection
- 📝 Custom filename support
- ⚙️ Built using Python and `yt-dlp`

## 🧰 Requirements

- Python 3.6 or later
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)

## 🧪 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/yt-dlp-gui-downloader.git
   cd yt-dlp-gui-downloader
   ```

2. **Install yt-dlp (if you haven't already)**:
   ```bash
   pip install -U yt-dlp
   ```

3. Run the application:
   ```bash
   python yt_downloader.py
   ```

## 📋 How to Use
1. Open the app.

2. Paste the YouTube video URL.

3. Click Browse to choose the folder to save the video.

4. Enter a filename (without .mp4 if you want; it will be added automatically).

5. Click Download and wait for the video to be saved!

## 🛑 Error Handling
If required fields are missing (URL, path, or filename), the app will show an error message. If yt-dlp fails, the full error is displayed for debugging.

## 📄 License
This project is licensed under the MIT License. Feel free to use, modify, and share it.

---

Made with ❤️ using Python and yt-dlp

_ZeroNeroIV_
