import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extractors.video_extractor import extract_video_text
from extractors.audio_extractor import extract_audio_text
from extractors.image_extractor import extract_image_text
from extractors.text_extractor import extract_text
from llm.gemini_client import ask_gemini


def process_file(path):
    path = path.lower()
    if path.endswith(('.pdf', '.docx', '.pptx', '.txt', '.md')):
        return extract_text(path)
    elif path.endswith(('.png', '.jpg', '.jpeg')):
        return extract_image_text(path)
    elif path.endswith(('.mp3', '.wav')):
        return extract_audio_text(path)
    elif path.endswith('.mp4'):
        return extract_video_text(path)
    else:
        print("❌ Unsupported file type.")
        return ""

if __name__ == "__main__":
    print("=== Multimodal Data Processing System ===")
    file_path = input("Enter file path (e.g. sample.pdf): ").strip()
    if not os.path.exists(file_path):
        print("File not found.")
        exit()

    print("\n🔄 Extracting data from file...")
    text_data = process_file(file_path)
    print("✅ Extraction complete.")

    while True:
        query = input("\nAsk a question (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        answer = ask_gemini(query, text_data)
        print("\n💬 Gemini says:", answer)
