import re
import json
from pathlib import Path

CLEANED_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\cleaned")
CHUNKS_DIR = Path(r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\chunks_legal")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

def split_by_headings(text):
    """
    Split text by legal headings like 'Rule', 'Section', 'Chapter'.
    Falls back to ~1000 char chunks if no headings found.
    """
    pattern = r"(Rule\s+\d+|Section\s+\d+|Chapter\s+[IVXLC]+)"
    parts = re.split(pattern, text)
    chunks = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ""
        chunks.append((heading, body))
    if not chunks:  # fallback
        chunks = [("Generic", text)]
    return chunks

def create_chunk_metadata(source_id, section, page, text, idx):
    return {
        "chunk_id": f"{source_id}_chunk_{idx:04d}",
        "source_id": source_id,
        "section": section,
        "page": page,
        "text": text
    }

def process_file(file_path):
    source_id = file_path.stem  # e.g. "PatentsAct1970_en"
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    chunks = split_by_headings(text)
    metadata_chunks = []
    for idx, (section, body) in enumerate(chunks, start=1):
        metadata_chunks.append(
            create_chunk_metadata(source_id, section, page=None, text=body, idx=idx)
        )
    return metadata_chunks

def chunk_all_files():
    for txt_file in CLEANED_DIR.rglob("*.txt"):
        print(f"Chunking (legal-aware): {txt_file.name}")
        metadata_chunks = process_file(txt_file)

        for chunk in metadata_chunks:
            chunk_path = CHUNKS_DIR / f"{chunk['chunk_id']}.json"
            with open(chunk_path, "w", encoding="utf-8") as f:
                json.dump(chunk, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(metadata_chunks)} chunks saved for {txt_file.name}")

if __name__ == "__main__":
    chunk_all_files()
