import os
from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3_trimmed(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        if filename.endswith(".mp4"):
            mp4_path = os.path.join(source_dir, filename)
            mp3_path = os.path.join(target_dir, filename.replace(".mp4", ".mp3"))

            try:
                video = VideoFileClip(mp4_path)
                duration = video.duration

                # Trim the last 3 seconds if video is longer than 3 seconds
                if duration > 3:
                    audio = video.subclip(0, duration - 3).audio
                else:
                    audio = video.audio

                audio.write_audiofile(mp3_path)
                audio.close()
                video.close()
                print(f"Saved: {mp3_path}")
            except Exception as e:
                print(f"Error with {filename}: {e}")

if __name__ == "__main__":
    source_folder = "./"       # folder with mp4s
    target_folder = "../mp3"   # folder to save mp3s
    convert_mp4_to_mp3_trimmed(source_folder, target_folder)
