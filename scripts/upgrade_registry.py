import pandas as pd

# Step 1: Read Excel and convert to CSV
excel_path = r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\metadata\source_registry.xlsx"
csv_path   = r"C:\Users\vaish\OneDrive\Desktop\sahayak\data\metadata\source_registry.csv"

# Read Excel (requires openpyxl installed)
df = pd.read_excel(excel_path)

# Step 2: Drop duplicate rows (same file_name + url)
df = df.drop_duplicates(subset=["file_name", "url"], keep="first")

# Step 3: Add new columns if missing
for col in ["source_id", "organization", "document_title", "publication_date"]:
    if col not in df.columns:
        df[col] = ""

# Step 4: Auto-generate source_id
df["source_id"] = [
    f"{row.source_name.replace(' ', '').upper()}_{i+1}"
    for i, row in enumerate(df.itertuples())
]

# Step 5: Fill organization (same as source_name for now)
df["organization"] = df["source_name"]

# Step 6: Fill document_title from file_name (basic cleanup)
df["document_title"] = (
    df["file_name"]
    .str.replace("_", " ")
    .str.replace(".pdf", "")
    .str.replace(".html", "")
    .str.strip()
)

# Step 7: Save as CSV
df.to_csv(csv_path, index=False)

print("✅ Registry upgraded and saved as CSV with source_id, organization, document_title")
