import os
import sys
import subprocess
import shutil

# 1. Image handling
try:
    from PIL import Image
except ImportError:
    Image = None

# 2. Audio handling
try:
    import mutagen
except ImportError:
    mutagen = None

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}
AUDIO_EXTENSIONS = {'.flac', '.mp3', '.wav', '.ogg'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.webm', '.avi'}

def get_ffmpeg_path():
    # 1. Check if bundled inside PyInstaller temp extraction directory (_MEIPASS)
    if hasattr(sys, '_MEIPASS'):
        bundled = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        if os.path.isfile(bundled):
            return bundled

    # 2. Check if ffmpeg.exe sits right next to the running executable / script
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    local_bin = os.path.join(base_dir, 'ffmpeg.exe')
    if os.path.isfile(local_bin):
        return local_bin

    # 3. Fall back to system PATH
    return shutil.which('ffmpeg')

def clean_image(filepath):
    filename = os.path.basename(filepath)
    if not Image:
        print(f"[SKIP IMAGE - Pillow missing] {filename}")
        return

    try:
        with Image.open(filepath) as img:
            data = list(img.getdata())
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(data)

            if 'transparency' in img.info:
                clean_img.info['transparency'] = img.info['transparency']

            temp_path = filepath + ".tmp"
            clean_img.save(temp_path)

        os.replace(temp_path, filepath)
        print(f"[CLEANED IMAGE] {filename}")
    except Exception as e:
        print(f"[FAILED IMAGE]  {filename}: {e}")

def clean_audio(filepath):
    filename = os.path.basename(filepath)
    if not mutagen:
        print(f"[SKIP AUDIO - Mutagen missing] {filename}")
        return

    try:
        audio = mutagen.File(filepath)
        if audio is not None and audio.tags:
            audio.delete()
            audio.save()
            print(f"[CLEANED AUDIO] {filename}")
        else:
            print(f"[NO TAGS AUDIO] {filename}")
    except Exception as e:
        print(f"[FAILED AUDIO]  {filename}: {e}")

def clean_video(filepath):
    filename = os.path.basename(filepath)
    ffmpeg_bin = get_ffmpeg_path()
    if not ffmpeg_bin:
        print(f"[SKIP VIDEO - FFmpeg not found] {filename}")
        return

    try:
        dir_name = os.path.dirname(filepath)
        temp_file = os.path.join(dir_name, f"clean_{os.path.basename(filepath)}")

        cmd = [
            ffmpeg_bin, "-y", "-v", "error",
            "-i", filepath,
            "-map_metadata", "-1",
            "-c", "copy",
            temp_file
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if res.returncode == 0:
            os.replace(temp_file, filepath)
            print(f"[CLEANED VIDEO] {filename}")
        else:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"[FAILED VIDEO]  {filename}: {res.stderr.decode(errors='ignore').strip()}")
    except Exception as e:
        print(f"[FAILED VIDEO]  {filename}: {e}")

def clean_item(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        clean_image(path)
    elif ext in AUDIO_EXTENSIONS:
        clean_audio(path)
    elif ext in VIDEO_EXTENSIONS:
        clean_video(path)

def main():
    items = sys.argv[1:]

    if not items:
        print("Universal Media Metadata Cleaner (Standalone)")
        print("Supports: Images (PNG/JPG/WEBP), Audio (FLAC/MP3/WAV/OGG), Video (MP4/MOV/MKV/WEBM)")
        print("\nDrag and drop files or folders directly onto this program's icon.")
        input("\nPress Enter to exit...")
        return

    for item in items:
        if os.path.isfile(item):
            clean_item(item)
        elif os.path.isdir(item):
            for root, _, files in os.walk(item):
                for f in files:
                    clean_item(os.path.join(root, f))

    print("\nProcessing complete!")
    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()