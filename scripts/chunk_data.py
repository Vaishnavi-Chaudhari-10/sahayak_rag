import os
from pathlib import Path

CLEANED_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\cleaned")
CHUNKS_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.
    - chunk_size: max characters per chunk
    - overlap: repeated characters between chunks for context continuity
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return chunk_text(text)

def chunk_all_files():
    for txt_file in CLEANED_DIR.rglob("*.txt"):
        print(f"Chunking: {txt_file.name}")
        chunks = process_file(txt_file)

        if not chunks:
            print(f"⚠️ No chunks created: {txt_file.name}")
            continue

        # Save each chunk as a separate file
        for i, chunk in enumerate(chunks, start=1):
            chunk_path = CHUNKS_DIR / f"{txt_file.stem}_chunk{i}.txt"
            with open(chunk_path, "w", encoding="utf-8") as f:
                f.write(chunk)

        print(f"✅ {len(chunks)} chunks saved for {txt_file.name}")

if __name__ == "__main__":
    chunk_all_files()
