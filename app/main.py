from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import create_vector_db, get_retriever
from app.generator import query_mistral
from app.memory import get_short_term_context, add_to_memory

PDF_PATH = "data/HSC26-Bangla1st-Paper.pdf"

create_vector_db(PDF_PATH)
retriever = get_retriever()

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_rag(query: Query):
    docs = retriever.get_relevant_documents(query.question)
    context = "\n\n".join([d.page_content for d in docs])
    chat_ctx = get_short_term_context()
    prompt = (
        "You are a strict QA assistant. Use ONLY the facts below.\n\n"
        f"Conversation History:\n{chat_ctx}\n\n"
        f"Knowledge:\n{context}\n\n"
        f"Question: {query.question}\n"
        "Answer in Bangla:"
    )
    answer = query_mistral(prompt)
    add_to_memory(query.question, answer)
    return {"answer": answer, "sources": [d.metadata for d in docs]}
