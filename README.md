# Indian Gender Budget RAG System

A Retrieval-Augmented Generation (RAG) system built over a corpus of Indian gender budget documents (PDFs, CSVs, and Excel files).

## Tech Stack
- Python, LangChain, ChromaDB, SentenceTransformers (`all-MiniLM-L6-v2`), Pandas.

## Project Structure
- `src/ingest.py` - Loads documents from `data/corpus`, chunks them, and builds the ChromaDB index in `index/`.
- `src/answer.py` - Evaluates questions from `questions_eval.jsonl` and generates outputs in `outputs/answers.jsonl`.
- `outputs/answers.jsonl` - Final generated evaluation answers with source citations.
- `SCOPE.md` - Project scope, inclusions, and limitations.
- `NOTES.md` - Implementation details and AI reflection.

## How to Run from a Clean Clone

```bash
# 1. Clone the Repository
git clone [https://github.com/razashoeb07/gender-budget-rag.git](https://github.com/razashoeb07/gender-budget-rag.git)
cd gender-budget-rag

# 2. Create and Activate Virtual Environment & Install Dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Run Ingestion and Evaluation Pipeline
python src/ingest.py
python src/answer.py