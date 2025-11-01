from moviepy import VideoFileClip

from .audio_extractor import extract_audio_text

def extract_video_text(file_path):
    clip = VideoFileClip(file_path)
    clip.audio.write_audiofile("temp.wav", logger=None)
    return extract_audio_text("temp.wav")
