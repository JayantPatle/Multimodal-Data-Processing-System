def ask_gemini(prompt, text_data):
    """
    Stub Gemini client used for local testing.

    Replace this with the real Gemini API call later.
    For now, it returns a simulated response so the rest
    of the system can work end-to-end.
    """
    snippet = (text_data or "").strip()

    if not snippet:
        return "(stub) No document text available."

    # Return a mock AI-style summary
    return f"(stub) AI Response to '{prompt}':\n\nSummary Preview:\n{snippet[:200]}..."
