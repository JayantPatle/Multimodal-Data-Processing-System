import streamlit as st
import os
import pytesseract
import logging
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from extractors.text_extractor import extract_text
from llm.gemini_client import ask_gemini
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tesseract path
TESSERACT_PATH = os.path.join(os.path.dirname(__file__), 'tools', 'Tesseract-OCR', 'tesseract.exe')

# Fallback sanitization to prevent prompt/stub leaks
def sanitize_response(resp: str) -> str:
    if not resp:
        return ""
    if not isinstance(resp, str):
        resp = str(resp)

    # Remove stub or echoed prompts
    resp = re.sub(r"^\(stub\).*", "", resp, flags=re.S)
    resp = re.sub(r"(?is)^Read the following.*?Content to summarize:.*", "", resp)
    resp = re.sub(r"(?i)summary preview:\s*", "", resp)

    return resp.strip()

# Extract audio or video
def extract_audio_text(filepath):
    r = sr.Recognizer()
    audio_filepath = None
    
    try:
        if filepath.endswith('.mp4'):
            video = VideoFileClip(filepath)
            audio_filepath = filepath.replace('.mp4', '.wav')
            video.audio.write_audiofile(audio_filepath)
            video.close()
        else:
            audio_filepath = filepath

        with sr.AudioFile(audio_filepath) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            return text

    except Exception as e:
        logger.error(f"Audio extraction failed: {e}")
        raise

    finally:
        if audio_filepath and filepath.endswith('.mp4'):
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)

# Initialize Tesseract
try:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except:
    pass

# Streamlit UI
st.set_page_config(page_title="Smart Content Analyzer", layout="centered")
st.title("📄 Smart Content Analyzer")
st.write("Upload any document, image, audio, or video — I’ll extract the text and generate a friendly, human-sounding summary.")

uploaded_file = st.file_uploader(
    "Choose a file to analyze",
    type=["txt", "pdf", "docx", "png", "jpg", "jpeg", "mp3", "mp4"]
)

if uploaded_file:
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, uploaded_file.name)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("📄 File uploaded successfully!")

    if st.button("✨ Generate Summary"):
        with st.spinner("Extracting content and generating your summary..."):
            try:
                # Routing per file extension
                if filepath.lower().endswith(('.mp3', '.mp4')):
                    extracted_text = extract_audio_text(filepath)
                else:
                    if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                        if not os.path.exists(TESSERACT_PATH):
                            raise Exception("Tesseract not found — OCR unavailable.")
                    extracted_text = extract_text(filepath)

                if not extracted_text:
                    st.error("No readable text found in this file.")
                else:
                    # Use Gemini 2.5 Flash
                    response = ask_gemini(
                        prompt="Summarize this content in a warm, simple, human tone within 500 words.",
                        text_data=extracted_text
                    )

                    clean = sanitize_response(response)

                    st.subheader("📝 Summary")
                    if clean:
                        st.markdown(clean)
                    else:
                        st.warning("The assistant didn't produce a summary. Try again.")

                    # File details
                    st.markdown("---")
                    size_kb = os.path.getsize(filepath) / 1024
                    st.write(f"**File type:** {filepath.split('.')[-1].upper()}")
                    st.write(f"**Size:** {size_kb:.1f} KB")
                    st.write(f"**Extracted characters:** {len(extracted_text)}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                logger.error(f"Error: {e}")

            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)

else:
    st.info("📎 Upload a file to start.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit & Gemini 2.5 Flash")