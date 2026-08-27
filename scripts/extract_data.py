import os
from pathlib import Path
from pypdf import PdfReader
import pymupdf  # modern import instead of fitz
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import langdetect

RAW_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\raw")
CLEAN_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\clean")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# Point to your installed Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def log_skip(file, reason):
    """Log skipped files with reason."""
    with open("skipped.log", "a", encoding="utf-8") as log:
        log.write(f"{file} → {reason}\n")

def extract_pdf_text(pdf_path):
    """Extract text from PDF, fallback to OCR if needed."""
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"⚠️ Skipping {pdf_path.name} (not a valid PDF): {e}")
        log_skip(pdf_path, str(e))
        return ""

    text_content = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            text_content.append(f"\n--- Page {page_num} ---\n{text}")
        else:
            # OCR fallback
            doc = pymupdf.open(pdf_path)
            pix = doc[page_num-1].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img, lang="eng+hin")
            text_content.append(f"\n--- Page {page_num} (OCR) ---\n{ocr_text}")
    return "\n".join(text_content)

def extract_html_text(html_path):
    """Extract visible text from HTML file."""
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        print(f"⚠️ Skipping {html_path.name} (HTML parse error): {e}")
        log_skip(html_path, str(e))
        return ""

def detect_language(text):
    """Detect dominant language of extracted text."""
    try:
        return langdetect.detect(text)
    except:
        return "unknown"

def process_all_files():
    for file in RAW_DIR.rglob("*"):
        text = ""
        if file.suffix.lower() == ".pdf":
            print(f"Extracting PDF: {file.name}")
            text = extract_pdf_text(file)
        elif file.suffix.lower() in [".html", ".htm"]:
            print(f"Extracting HTML: {file.name}")
            text = extract_html_text(file)
        else:
            continue

        if not text.strip():
            log_skip(file, "No text extracted")
            continue

        lang = detect_language(text)
        clean_path = CLEAN_DIR / f"{file.stem}_{lang}.txt"
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Saved extracted text ({lang}) → {clean_path}")

if __name__ == "__main__":
    process_all_files()
