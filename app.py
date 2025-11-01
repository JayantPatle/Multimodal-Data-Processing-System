import streamlit as st
import os
import pytesseract
import logging
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from extractors.text_extractor import extract_text
from llm.gemini_client import ask_gemini

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set custom Tesseract path
TESSERACT_PATH = os.path.join(os.path.dirname(__file__), 'tools', 'Tesseract-OCR', 'tesseract.exe')

def extract_audio_text(filepath):
    """Extract text from audio/video files"""
    r = sr.Recognizer()
    audio_filepath = None
    
    try:
        logger.info(f"Processing audio/video file: {filepath}")
        
        if filepath.endswith('.mp4'):
            try:
                # Extract audio from video
                video = VideoFileClip(filepath)
                audio_filepath = filepath.replace('.mp4', '.wav')
                video.audio.write_audiofile(audio_filepath)
                video.close()
                logger.info(f"Audio extracted to: {audio_filepath}")
            except Exception as e:
                logger.error(f"Video processing failed: {str(e)}")
                raise
        else:
            audio_filepath = filepath

        # Convert audio to text
        try:
            with sr.AudioFile(audio_filepath) as source:
                audio = r.record(source)
                text = r.recognize_google(audio)
                logger.info("Audio transcription successful")
                return text
        except Exception as e:
            logger.error(f"Speech recognition failed: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Audio extraction failed: {str(e)}")
        raise
    
    finally:
        # Cleanup temporary files
        if audio_filepath and filepath.endswith('.mp4'):
            if os.path.exists(audio_filepath):
                os.remove(audio_filepath)
                logger.info(f"Cleaned up temporary file: {audio_filepath}")

# Initialize Tesseract
try:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    logger.info(f"Tesseract initialized at: {TESSERACT_PATH}")
except Exception as e:
    logger.error(f"Tesseract initialization failed: {e}")

# Streamlit UI Configuration
st.set_page_config(page_title="Smart Content Analyzer", layout="centered")
st.title("📄 Smart Content Analyzer")
st.markdown("*Supports documents, images, audio, and video files*")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your file",
    type=["txt", "pdf", "docx", "png", "jpg", "mp3", "mp4"]
)

if uploaded_file:
    # Create upload directory
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, uploaded_file.name)
    
    # Save uploaded file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("✅ File uploaded successfully!")

    if st.button("Analyze Content"):
        with st.spinner("Processing..."):
            try:
                # Handle different file types
                if filepath.lower().endswith(('.mp3', '.mp4')):
                    extracted_text = extract_audio_text(filepath)
                else:
                    # Verify Tesseract for image files
                    if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                        if not os.path.exists(TESSERACT_PATH):
                            raise Exception("Tesseract OCR is not installed in tools/Tesseract-OCR")
                    extracted_text = extract_text(filepath)

                if not extracted_text:
                    st.error("No content could be extracted")
                else:
                    # Get analysis from Gemini
                    response = ask_gemini(
                    prompt=(
                    "Read the following content carefully and write a concise, well-structured summary "
                    "in simple English within 100 words. Focus on the main ideas, key points, and overall meaning. "
                    "Avoid unnecessary details, repetitions, or examples. "
                    "Ensure the tone is professional and easy to understand.\n\n"
                    "Content to summarize:"
                    ),
                        text_data=extracted_text
                    )
                    
                    # Display results
                    st.subheader("🔍 Analysis Results:")
                    st.markdown(response)
                    
                    # Show file info
                    st.markdown("---")
                    file_size = os.path.getsize(filepath) / 1024
                    st.markdown("**File Information:**")
                    st.markdown(f"- Type: {os.path.splitext(filepath)[1][1:].upper()}")
                    st.markdown(f"- Size: {file_size:.1f} KB")
                    st.markdown(f"- Content Length: {len(extracted_text)} characters")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error(f"Process failed: {str(e)}")

            finally:
                # Cleanup
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Cleaned up: {filepath}")
else:
    st.info("📎 Upload a file to begin analysis")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit and Google Gemini AI*")