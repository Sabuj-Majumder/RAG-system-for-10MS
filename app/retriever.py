from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from app.pdf_loader import load_and_preprocess

def create_vector_db(pdf_path: str,
                     model_id: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    docs_meta = load_and_preprocess(pdf_path)
    docs = [
        Document(page_content=d["content"], metadata={"question_id": d["question_id"]})
        for d in docs_meta
    ]
    embed = HuggingFaceEmbeddings(model_name=model_id)
    db = FAISS.from_documents(docs, embed)
    db.save_local("faiss_index")
    print(f"✅ Indexed {len(docs)} chunks into FAISS")

def get_retriever():
    embed = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    db = FAISS.load_local("faiss_index", embed, allow_dangerous_deserialization=True)
    return db.as_retriever()
