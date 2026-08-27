import re
from pathlib import Path

EXTRACTED_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\clean")
FINAL_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\cleaned")
FINAL_DIR.mkdir(parents=True, exist_ok=True)

def normalize_text(text):
    """Clean whitespace and remove clutter while preserving multilingual characters."""
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove page markers like '--- Page 12 ---'
    text = re.sub(r"--- Page \d+.*---", "", text)

    # Remove standalone page numbers
    text = re.sub(r"\bPage \d+\b", "", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Deduplicate consecutive identical lines
    lines = text.splitlines()
    deduped = []
    for line in lines:
        if not deduped or line.strip() != deduped[-1].strip():
            deduped.append(line)
    text = "\n".join(deduped)

    return text.strip()

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return normalize_text(text)

def clean_all_files():
    for txt_file in EXTRACTED_DIR.rglob("*.txt"):
        print(f"Cleaning: {txt_file.name}")
        text = process_file(txt_file)

        if not text:
            print(f"⚠️ No text extracted: {txt_file.name}")
            continue

        output_path = FINAL_DIR / txt_file.name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Cleaned file saved → {output_path}")

if __name__ == "__main__":
    clean_all_files()


# Cleaning →

# Normalizes whitespace and line breaks.

# Removes page markers (--- Page N ---).

# Removes stray page numbers.

# Deduplicates repeated lines.

# Preserves Hindi and other multilingual text.