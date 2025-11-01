import pytesseract, cv2

def extract_image_text(file_path):
    img = cv2.imread(file_path)
    if img is None: return ""
    return pytesseract.image_to_string(img)
