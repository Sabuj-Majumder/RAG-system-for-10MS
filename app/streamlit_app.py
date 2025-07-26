
import os, sys
import streamlit as st
import requests


API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Bangla RAG Q&A", layout="centered")
st.title("📚 Bangla RAG Q&A System")
st.write("Ask questions in Bangla or English based on the HSC26 Bangla 1st‑Paper PDF.")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please type a question before hitting Ask.")
    else:
        with st.spinner("Calling the RAG API..."):
            try:
                resp = requests.post(API_URL, json={"question": question})
                resp.raise_for_status()
            except Exception as e:
                st.error(f"Failed to reach the API: {e}")
            else:
                data = resp.json()
                answer = data.get("answer", "")
                sources = data.get("sources", [])

               
                st.markdown("### 💬 Answer")
                if answer:
                    st.success(answer)
                else:
                    st.info("উত্তর পাওয়া যায়নি")

               
                st.markdown("### 📑 Sources Retrieved")
                for src in sources:
                    qid = src.get("question_id", "―")
                    st.write(f"- Chunk **{qid}**")
