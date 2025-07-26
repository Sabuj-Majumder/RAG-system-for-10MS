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
```bash
bilingual_rag_system_2/
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
















