# NOTES.md

## System Architecture
The system uses a local retrieval-augmented pipeline powered by `SentenceTransformerEmbeddings` (`all-MiniLM-L6-v2`) and a persistent `ChromaDB` vector store. Documents are processed using custom data loaders in Python, utilizing `PyPDFLoader` for PDF documents and `Pandas` (with `latin1` encoding fallback) for CSV and Excel files. Documents are split using `RecursiveCharacterTextSplitter` with a chunk size of 1000 and overlap of 200.

## AI Reflection (Misleading AI Output & Fix)
During the initial development of the ingestion pipeline, an AI assistant recommended using `UnstructuredExcelLoader` to parse `.xls` spreadsheet files. However, executing this on Windows led to critical build and dependency failures (`ModuleNotFoundError: No module named 'unstructured'` and missing system-level C++ binaries). 

I caught this blocker by inspecting the terminal traceback errors during execution. To overcome this, I replaced the unstructured loader with `pandas.read_excel()` and `pandas.read_csv(encoding='latin1')`. This lightweight approach parsed all tabular data row-by-row into `Document` objects without requiring heavy native system drivers.

## Next Steps with More Time
- Integrate a local generation model (e.g., Llama 3 / Mistral via Ollama) or hosted LLM API to summarize precise numerical figures instead of outputting contextual matches.
- Add PaddleOCR/Tesseract to extract Hindi text embedded inside scanned government PDF tables.
- Implement table structure preservation for financial matrices instead of flat key-value row representation.