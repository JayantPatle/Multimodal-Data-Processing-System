# Multimodal Data Processing System

A small Python utility to extract text from multiple file types (PDF, DOCX, PPTX, TXT/MD, images, audio, video) and query the extracted content using a simple Gemini client stub.

## Project layout

- `main.py` — CLI runner. Asks for a file path, extracts text with the appropriate extractor, then prompts the user for questions to send to the Gemini client.
- `app.py` — (optional) web UI entrypoint if present.
- `extractors/` — collection of extractors:
  - `text_extractor.py` — PDF/DOCX/PPTX/TXT extraction (uses PyMuPDF, python-docx, python-pptx)
  - `image_extractor.py` — image OCR (uses pytesseract + Pillow/OpenCV)
  - `audio_extractor.py` — audio transcription (uses SpeechRecognition)
  - `video_extractor.py` — video -> audio -> transcription (uses moviepy/imageio-ffmpeg)
- `llm/gemini_client.py` — local stub `ask_gemini(query, text_data)` used by `main.py` (replace this with a real client when available).
- `requirements.txt` — pinned Python packages used by the project.

## What this README helps with

- Set up a virtual environment
- Install Python dependencies
- Install required system binaries (Tesseract, FFmpeg)
- Run the CLI and test extraction
- Troubleshoot common errors

---

## Requirements

- Python 3.10+ (project was tested on Python 3.12 in the provided virtualenv)
- The Python packages listed in `requirements.txt`. Create a virtual environment and install them.
- System binaries (outside pip) for some extractors:
  - Tesseract OCR (for `pytesseract`) — https://github.com/tesseract-ocr/tesseract
  - FFmpeg (for moviepy/imageio-ffmpeg) — https://ffmpeg.org/

If you are on Windows, add the Tesseract and FFmpeg executables to your PATH so the Python wrappers can find them.

## Setup (Windows PowerShell)

Open PowerShell in the project root (`d:\multimodal_data_system`) and run:

```powershell
# create a venv (if you don't have one already)
python -m venv venv
# activate it
.\venv\Scripts\Activate.ps1
# install packages
pip install -r requirements.txt
```

If you already have the project's virtualenv at `D:/multimodal_data_system/venv`, use the existing Python executable directly:

```powershell
D:/multimodal_data_system/venv/Scripts/python.exe -m pip install -r requirements.txt
D:/multimodal_data_system/venv/Scripts/Activate.ps1
```

## Run the CLI

From the project root (with the venv active):

```powershell
python main.py
```

Example session:

1. When prompted, enter the full path to a file to extract (e.g. `C:\Users\You\Downloads\sample.pdf`).
2. After extraction, ask questions about the document. Type `exit` to quit.

Notes: `main.py` expects a file path readable from the current system. If `File not found.` appears, supply an absolute path or ensure your working directory is correct.

## How the LLM client works (current state)

The project includes a stub in `llm/gemini_client.py`:

```python
# llm/gemini_client.py
def ask_gemini(query, text_data):
    # stub — replace with actual call to a cloud LLM or other local model
    return "(stub) ..."
```

Replace this function with your actual LLM client or integrate with the official SDK you intend to use.

## Troubleshooting

- "File not found." — Use an absolute path or verify the relative path from your current working directory.
- Missing Tesseract errors (pytesseract) — Install Tesseract and add it to PATH. On Windows, you may need to set `pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"` in `extractors/image_extractor.py` if not on PATH.
- FFmpeg errors — Install FFmpeg and ensure it is on PATH. moviepy will try to use it to read/write audio/video.
- Permission errors — Ensure the process can read the file.
- Encoding errors reading text files — ensure the files are UTF-8 or adapt `open(..., encoding=...)` in `extractors/text_extractor.py`.
- `ask_gemini` not defined — Ensure `from llm.gemini_client import ask_gemini` is present in `main.py`. (This project includes that import by default.)

## Testing / Quick checks

- Run a minimal extraction from Python REPL:

```powershell
# from project root with venv active
python -c "from extractors.text_extractor import extract_text; print(extract_text('samples/test.txt'))"
```

- Check your Python environment details (useful when debugging package issues):

```powershell
python -c "import sys, pkgutil; print(sys.executable); import pkg_resources; print('\n'.join(sorted([p.project_name for p in pkg_resources.working_set])))"
```

## Extending the project

- Replace `llm/gemini_client.py` with a proper implementation that calls a cloud LLM or local model.
- Improve error handling in extractors (wrap file reads in try/except and return helpful messages).
- Add unit tests for extractors and a small integration test for `main.py`.

## Contributing

Feel free to open issues or PRs. Keep changes small and focused. Add tests for any new extractor or major logic change.

## License

This project doesn't include a license file. Add one (for example, `MIT`) to clarify reuse terms.

---


![Multimodal Data Processing System Screenshot](\screenshot\Screenshot.png)