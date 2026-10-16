# ============================================================
# IMPORT REQUIRED LIBRARIES
# ============================================================

import os
import pandas as pd

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "data/corpus"
DB_PATH = "index"


# ============================================================
# LOAD CUSTOM DOCUMENTS
# ============================================================

def load_custom_documents():
    documents = []

    # --------------------------------------------------------
    # 1. LOAD PDF FILES USING PyPDFLoader
    # --------------------------------------------------------

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)

        if file.endswith(".pdf"):
            print(f"Loading PDF: {file}")
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

        # ----------------------------------------------------
        # 2. LOAD CSV FILES USING PANDAS
        # ----------------------------------------------------

        elif file.endswith(".csv"):
            print(f"Loading CSV: {file}")
            df = pd.read_csv(file_path, encoding='latin1')

            for index, row in df.iterrows():
                content = " ".join(
                    [
                        f"{col}: {val}"
                        for col, val in row.items()
                        if pd.notna(val)
                    ]
                )

                documents.append(
                    Document(
                        page_content=content,
                        metadata={"source": file, "row": index}
                    )
                )

        # ----------------------------------------------------
        # 3. LOAD EXCEL FILES (.xls / .xlsx) USING PANDAS
        # ----------------------------------------------------

        elif file.endswith((".xls", ".xlsx")):
            print(f"Loading Excel: {file}")

            try:
                df = pd.read_excel(file_path, sheet_name=0)

                for index, row in df.iterrows():
                    content = " ".join(
                        [
                            f"{col}: {val}"
                            for col, val in row.items()
                            if pd.notna(val)
                        ]
                    )

                    documents.append(
                        Document(
                            page_content=content,
                            metadata={"source": file, "row": index}
                        )
                    )

            except Exception as e:
                print(f"Error reading excel {file}: {e}")

    return documents


# ============================================================
# DOCUMENT INGESTION PIPELINE
# ============================================================

def ingest_documents():

    # --------------------------------------------------------
    # 1. LOAD DOCUMENTS
    # --------------------------------------------------------

    print("Documents load ho rahe hain...")

    all_docs = load_custom_documents()
    print(f"Total {len(all_docs)} documents/rows load hue hain.")

    # --------------------------------------------------------
    # 2. SPLIT DOCUMENTS INTO TEXT CHUNKS
    # --------------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(all_docs)
    print(f"Total {len(chunks)} chunks ban gaye hain.")

    # --------------------------------------------------------
    # 3. INITIALIZE EMBEDDING MODEL
    # --------------------------------------------------------

    print("Vector database ban raha hai...")

    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # --------------------------------------------------------
    # 4. CREATE CHROMA VECTOR DATABASE
    # --------------------------------------------------------

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_PATH
    )

    # --------------------------------------------------------
    # 5. INGESTION COMPLETED
    # --------------------------------------------------------

    print("Ingestion complete! Database 'index' folder mein save ho gaya hai.")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    ingest_documents()