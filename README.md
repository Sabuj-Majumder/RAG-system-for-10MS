# Bilingual RAG Q&A System

A Retrieval‑Augmented Generation (RAG) system that accepts Bangla or English questions and answers them based on the **HSC26 Bangla 1st‑Paper** PDF.  
Built with free, open‑source tools for fully offline use.

---

## 📖 Project Overview

- **Input**: User question (Bangla or English)  
- **Retrieval**: FAISS vector index over PDF‑derived chunks  
- **Generation**: Local LLM (Mistral via Ollama)  
- **Short‑Term Memory**: Recent chat history  
- **Long‑Term Memory**: PDF corpus in FAISS  

---

## 🚀 Features

- ✅ **Bilingual** (Bangla & English) question answering  
- ✅ **OCR**‑backed PDF ingestion (via Tesseract + Poppler)  
- ✅ **Semantic retrieval** using FAISS & multilingual embeddings  
- ✅ **Context‑strict prompting** for grounded answers  
- ✅ **Streamlit UI** & **FastAPI** backend  
- ✅ Fully **local/offline**—no paid APIs required  

---

## 📂 Directory Structure
```
RAG-system-for-10MS/
│
├── app/                         # Core application modules
│   ├── __init__.py              # Marks this as a Python package
│   ├── pdf_loader.py            # PDF → clean text → chunks
│   ├── retriever.py             # Build & load FAISS index
│   ├── generator.py             # Ollama/Mistral invocation
│   ├── memory.py                # Short‑term chat memory
│   ├── main.py                  # FastAPI app (/ask endpoint)
│   ├── streamlit_app.py         # Streamlit UI
│   └── requirements.txt         # Python deps for app/
│
├── data/                        
│   └── HSC26-Bangla1st-Paper.pdf # Input PDF
│
├── faiss_index/                 # (auto‑generated) FAISS files
├── evaluation/                  # RAG evaluation scripts
│   └── evaluate_rag.py
├── Dockerfile                   # Container spec
├── docker-compose.yml           # Service orchestration
└── README.md                    # ← You are here
```
--- 

# 🛠 Prerequisites
- Python 3.10+

- Tesseract OCR

- Windows: install via .exe and add to PATH

- Linux/macOS: sudo apt install tesseract-ocr tesseract-ocr-ben

- Poppler (for pdf2image)

- Windows: download/extract & add Library\bin to PATH

- Linux/macOS: sudo apt install poppler-utils

- Ollama (for local Mistral model)

- Install instructions

- Run ollama run mistral in the background
---


# ⚙️ Installation
## 1. Clone the repo :
```
git clone https://github.com/Sabuj-Majumder/RAG-system-for-10MS
```
## 2. Create & activate a virtual environment
```
python -m venv venv
# Windows
.\venv\Scripts\Activate
# macOS/Linux
source venv/bin/activate
```
## 3.Install dependencies
```
pip install --upgrade pip
pip install -r app/requirements.txt
```
## 4.Verify tools
```
tesseract --version
pdftoppm -v       # Poppler tool
ollama run mistral # start Mistral model
```
---

# ▶️ Running Locally:
## 1. Start the FastAPI backend
```
uvicorn app.main:app --reload
```
- Endpoint: POST http://localhost:8000/ask

- Request:
```
  { "question": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?" }
```
- Response:
```
{
  "answer": "শুম্ভুনাথ",
  "sources": [
    { "question_id": "১." },
    ...
  ]
}
```
---

# 2. Launch the Streamlit UI
## In another terminal:
```
streamlit run app/streamlit_app.py
```
Open your browser at http://localhost:8501 to ask questions interactively.
# 🐳 Docker Deployment (Optional)
## Build & run both services via Docker Compose:
```
docker-compose up --build

```
- FastAPI → http://localhost:8000

- Streamlit UI → http://localhost:8501

---

# 🔧 Configuration

- PDF path: in app/main.py (constant PDF_PATH)

- Tesseract: adjust pytesseract.pytesseract.tesseract_cmd in app/pdf_loader.py

- Poppler: adjust POPPLER_PATH in app/pdf_loader.py

- Embedding model: change model_name in app/retriever.py

- LLM & temperature: change "--temperature", "0" in app/generator.py

---


# 🧪 RAG Evaluation
We provide a simple evaluation script to measure Relevance and Groundedness.

## 1. Define test cases
Edit evaluation/evaluate_rag.py to add your own queries, expected answers, and expected question‑IDs.

## 2. Run the evaluation
```
python evaluation/evaluate_rag.py
```
Metrics reported per case:

- Relevance Score: Cosine similarity between the query and retrieved chunk

- Chunk Match: Whether the retrieved chunk’s ID matches the expected ID

- Generated Answer: The model’s response

- Answer Correctness: Whether the expected answer string appears in the generated answer

- Groundedness Score: Cosine similarity between the generated answer and the retrieved context

## ample output:
```
----------------------------------------
Query: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
Expected chunk: ১. | Retrieved: ১. (Relevance=0.72)
Expected answer: শুম্ভুনাথ
Generated answer: শুম্ভুনাথ
Answer correct? True, Groundedness=0.65
...
Overall metrics:
  Avg. Relevance:    0.68
  Avg. Groundedness: 0.61
```
---
# 🛠 Troubleshooting
## Import errors (ModuleNotFoundError)
- Ensure you run Streamlit & Uvicorn from the project root, and that app/__init__.py exists.

## OCR garbage output
- Tweak DPI (600 → 800), PSM mode (--psm 3), or add custom corrections in app/pdf_loader.py.

## Wrong retrieval
- Increase k in get_retriever().as_retriever(k=6) or adjust chunk boundaries.

## Hallucinations
- Use zero temperature (--temperature 0) and strict “Answer only from context” prompts.
