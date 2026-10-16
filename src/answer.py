# ============================================================
# IMPORT REQUIRED LIBRARIES
# ============================================================

import json
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "index"
EVAL_PATH = "questions_eval.jsonl"
OUTPUT_PATH = "outputs/answers.jsonl"


# ============================================================
# GENERATE ANSWERS
# ============================================================

def generate_answers():

    # --------------------------------------------------------
    # 1. LOAD EMBEDDING MODEL AND VECTOR DATABASE
    # --------------------------------------------------------

    print("Loading vector database...")

    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    # --------------------------------------------------------
    # 2. CREATE OUTPUT DIRECTORY IF IT DOES NOT EXIST
    # --------------------------------------------------------

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # --------------------------------------------------------
    # 3. LOAD AND EVALUATE QUESTIONS
    # --------------------------------------------------------

    print("Evaluating questions from questions_eval.jsonl...")

    results = []

    with open(EVAL_PATH, "r", encoding="utf-8") as f:
        for line in f:

            if not line.strip():
                continue

            q_data = json.loads(line)

            q_id = q_data["question_id"]
            question_text = q_data["question"]

            # ------------------------------------------------
            # 4. RETRIEVE TOP MATCHING DOCUMENTS
            # ------------------------------------------------

            docs = retriever.invoke(question_text)

            # ------------------------------------------------
            # 5. EXTRACT SOURCE INFORMATION AND CONTENT
            # ------------------------------------------------

            sources = []
            combined_content = ""

            for doc in docs:
                source_file = os.path.basename(
                    doc.metadata.get("source", "unknown")
                )

                page_num = doc.metadata.get("page", 0) + 1  # 1-indexed page conversion

                sources.append({
                    "file": source_file,
                    "page": page_num
                })

                combined_content += doc.page_content + "\n"

            # ------------------------------------------------
            # 6. FORMULATE OUTPUT FORMAT
            # ------------------------------------------------

            # Formulating output format as required by the assignment
            answered = True if docs else False

            answer_text = (
                f"Context found for: {question_text}"
                if answered
                else ""
            )

            results.append({
                "question_id": q_id,
                "answered": answered,
                "answer": answer_text,
                "sources": sources[:1]  # Taking top source
            })

    # --------------------------------------------------------
    # 7. SAVE ANSWERS TO JSONL FILE
    # --------------------------------------------------------

    # Save to outputs/answers.jsonl
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_f:
        for res in results:
            out_f.write(
                json.dumps(res, ensure_ascii=False) + "\n"
            )

    # --------------------------------------------------------
    # 8. DISPLAY COMPLETION MESSAGE
    # --------------------------------------------------------

    print(
        f"Answers successfully generated and saved to {OUTPUT_PATH}!"
    )


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    generate_answers()