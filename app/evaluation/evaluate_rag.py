import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from app.retriever import get_retriever
from app.generator import query_mistral
EMBED_MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


retriever = get_retriever()

TEST_CASES = [
    {
        "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
        "expected_answer": "শুম্ভুনাথ",
        "expected_qid": "১."
    },
    {
        "query": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
        "expected_answer": "মামাকে",
        "expected_qid": "২."
    },
    {
        "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
        "expected_answer": "১৫ বছর",
        "expected_qid": "৫."
    },
]

def embed(texts):
    """Embed a list of strings and return a numpy array."""
    return EMBED_MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def evaluate_case(case):
    q = case["query"]
    exp_ans = case["expected_answer"]
    exp_qid = case["expected_qid"]


    docs = retriever.get_relevant_documents(q)
    contents = [d.page_content for d in docs]
    qid_list  = [d.metadata.get("question_id") for d in docs]

  
    q_vec = embed([q])[0]
    chunk_vecs = embed(contents)
    relevances = cosine_similarity([q_vec], chunk_vecs)[0]

    best_idx = np.argmax(relevances)
    best_qid = qid_list[best_idx]
    best_relevance = relevances[best_idx]


    prompt = f"""
Use ONLY the context below to answer the question. If not found, answer “উত্তর পাওয়া যায়নি”.

Context:
{contents[best_idx]}

Question: {q}

Answer in Bangla:
"""
    answer = query_mistral(prompt)

  
    concat_ctx = " ".join(contents[:3])
    ans_vec = embed([answer])[0]
    ctx_vec = embed([concat_ctx])[0]
    groundedness = cosine_similarity([ans_vec], [ctx_vec])[0][0]

    # Compare to expected
    is_correct_ans = exp_ans in answer
    is_correct_chunk = (best_qid == exp_qid)

    return {
        "query": q,
        "retrieved_qid": best_qid,
        "expected_qid": exp_qid,
        "relevance_score": float(best_relevance),
        "groundedness_score": float(groundedness),
        "generated_answer": answer,
        "expected_answer": exp_ans,
        "answer_contains_expected": is_correct_ans,
        "chunk_match": is_correct_chunk
    }

def main():
    results = []
    for case in TEST_CASES:
        res = evaluate_case(case)
        results.append(res)
        print("—" * 40)
        print(f"Query: {res['query']}")
        print(f"Expected chunk: {res['expected_qid']} | Retrieved: {res['retrieved_qid']} (Relevance={res['relevance_score']:.3f})")
        print(f"Expected answer: {res['expected_answer']}")
        print(f"Generated answer: {res['generated_answer']}")
        print(f"Answer correct? {res['answer_contains_expected']}, Groundedness={res['groundedness_score']:.3f}")
  
    avg_rel = np.mean([r["relevance_score"] for r in results])
    avg_grd = np.mean([r["groundedness_score"] for r in results])
    print("\nOverall metrics:")
    print(f"  Avg. Relevance:    {avg_rel:.3f}")
    print(f"  Avg. Groundedness: {avg_grd:.3f}")

if __name__ == "__main__":
    main()
