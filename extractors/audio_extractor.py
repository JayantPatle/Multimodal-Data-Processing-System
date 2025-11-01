import speech_recognition as sr

def extract_audio_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as src:
        audio = r.record(src)
    return r.recognize_google(audio)
