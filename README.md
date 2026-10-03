# AI Audio Visual Metadata Eraser

A lightweight, zero-dependency, drag-and-drop Windows utility designed to losslessly scrub AI generation prompts, ComfyUI workflow JSON, camera tags, and identifying metadata from production media assets.

---

## Features

- **True Drag-and-Drop:** Drop single files, multiple selections, or entire nested folders directly onto the application icon.
- **Lossless Processing:** 
  - Videos are remuxed using stream copying (`-c copy`) without re-encoding or quality degradation.
  - Audio container comments and ID3/Vorbis tags are wiped in place.
  - Image metadata blocks (EXIF, text chunks) are stripped while maintaining pixel integrity.
- **Self-Contained:** Python and FFmpeg are bundled directly inside the executable. No separate installations or PATH configurations required.

---

## Supported Formats

| Media Type | Formats Supported |
| :--- | :--- |
| **Video** | `.mp4`, `.mov`, `.mkv`, `.webm`, `.avi` |
| **Audio** | `.flac`, `.mp3`, `.wav`, `.ogg` |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff` |

*(Note: Designed specifically for multimedia assets. Office and document formats such as PDF, DOCX, or project project files like .prproj are not processed.)*

---

## How to Use

1. Go to the **[Releases](../../releases)** tab on GitHub.
2. Download `AIAudioVisualMetadataEraser.exe`.
3. Place the `.exe` anywhere convenient (such as your Desktop).
4. Drag and drop any supported media file, batch of files, or directory directly onto the `.exe` icon.
5. A console window will show the cleaning status for each file and prompt to close once finished.

---

## How to Verify Your Files Are Clean

Windows File Explorer often hides deep container atoms or caches old metadata tags. To independently verify that prompts, workflows, and encoder tags have been wiped:

1. Download the free, open-source tool **[MediaInfo](https://mediaarea.net/MediaInfo)** (or use their browser version at [mediaarea.net/MediaInfoOnline](https://mediaarea.net/MediaInfoOnline)).
2. Open MediaInfo and switch the view to **View → Text** or **View → Tree**.
3. Inspect your file before and after running it through the cleaner:
   - **Before:** Look for sections containing `Workflow`, `Prompt`, `Lavf`, `Title`, or `Comment`.
   - **After:** Those blocks will be completely absent—only essential playback parameters (codecs, bitrates, dimensions) remain.

---

## Windows SmartScreen / Antivirus Notice

Because this application is a newly compiled open-source tool without an expensive commercial code-signing certificate, Windows SmartScreen may show a prompt saying:

> *"Windows protected your PC — Unknown publisher"*

**To run the tool:**
1. Click **More info**.
2. Click **Run anyway**.

The full Python source code is provided in this repository for complete transparency and independent verification.

---

## Running from Source

If you prefer running or building the script yourself:

```bash
# Clone the repository
git clone [https://github.com/YourUsername/ai-audio-visual-metadata-eraser.git](https://github.com/YourUsername/ai-audio-visual-metadata-eraser.git)
cd ai-audio-visual-metadata-eraser

# Install dependencies
pip install pillow mutagen

# Run the script
python drag_drop_cleaner.py [file_or_folder_path]
