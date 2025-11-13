import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_SECRET") 

if not API_KEY:
    raise RuntimeError("GEMINI_API_SECRET is missing. Add it in .env or system environment.")

# Configure Gemini
genai.configure(api_key=API_KEY)

def ask_gemini(prompt, text_data=""):
    """
    Humanized, clean summarization generator using Gemini 2.5 Flash.
    Returns ONLY the model output (no prompts, no stubs, no labels).
    """

    model = genai.GenerativeModel("gemini-2.5-flash")  # 🔥 Updated model

    final_prompt = (
        "You are a clear, friendly assistant. "
        "Write a human-sounding summary that is warm, simple, and easy to read. "
        "Avoid repeating the instructions or including this prompt in the output.\n\n"
        "CONTENT:\n"
        f"{text_data}\n\n"
        "SUMMARY INSTRUCTION:\n"
        f"{prompt}\n\n"
        "Return only the final summary. No labels, no extra explanations."
    )

    try:
        resp = model.generate_content(final_prompt)
        # The SDK returns .text in latest version
        return resp.text.strip()
    except Exception as e:
        return f"Error from Gemini: {e}"