import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(query, context=""):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Context:\n{context}\n\nQuestion: {query}")
    return response.text
