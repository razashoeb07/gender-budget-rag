# Project Scope

This project implements a Retrieval-Augmented Generation (RAG) system specifically designed for Indian Gender Budget documents.

## Key Features
- **Data Support**: Heterogeneous document parsing including PDFs, CSVs, and Excel spreadsheets.
- **Embeddings & Vector Database**: Uses SentenceTransformers (`all-MiniLM-L6-v2`) paired with ChromaDB for efficient semantic vector storage and document retrieval.
- **Output Format**: Structured evaluation response generation producing valid `.jsonl` files specifying `question_id`, `answered` flag, context `answer`, and source citations.