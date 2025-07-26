import fitz                         
import re
import unicodedata
from pdf2image import convert_from_path
import pytesseract

# ─── CONFIG ────────────────────────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\tools\poppler-24.08.0\Library\bin"
# ───────────────────────────────────────────────────────────────────────

def extract_clean_text(pdf_path: str) -> str:

    doc = fitz.open(pdf_path)
    raw = "\n".join(page.get_text("text") for page in doc)

    if len(re.findall(r"[\u0980-\u09FF]", raw)) < 200:
        images = convert_from_path(pdf_path, dpi=1000, poppler_path=POPPLER_PATH)
        config = "--oem 1 --psm 3"
        for img in images:
            raw += pytesseract.image_to_string(img, lang="ben+eng", config=config)


    text = unicodedata.normalize("NFC", raw)
    text = text.replace("-\n", "").replace("\n", " ")
    text = re.sub(r"[^\u0980-\u09FFa-zA-Z0-9।?!,.: \s]+", "", text)
    return re.sub(r"\s+", " ", text).strip()

def chunk_by_question(text: str) -> list[dict]:

    parts = re.split(r"(?=(?:\d|[১২৩৪৫৬৭৮৯০])+\.)", text)
    docs = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        qid = p.split()[0]
        docs.append({"question_id": qid, "content": p})
    return docs

def load_and_preprocess(pdf_path: str) -> list[dict]:
    cleaned = extract_clean_text(pdf_path)
    return chunk_by_question(cleaned)

if __name__ == "__main__":
    chunks = load_and_preprocess("data/HSC26-Bangla1st-Paper.pdf")
    with open("output.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(f"{c['question_id']} {c['content']}\n\n")
    print(f"✅ Extracted {len(chunks)} chunks — see output.txt")
