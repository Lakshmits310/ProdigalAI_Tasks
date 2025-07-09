import os
import faiss
from sentence_transformers import SentenceTransformer
import PyPDF2

# Directory for saving FAISS index and chunk texts
EMBEDDING_DIR = "../embeddings/"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyPDF2."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join(page.extract_text() or "" for page in reader.pages)
    print("✅ Extracted Text Preview:\n", text[:1000])
    return text

def chunk_text(text, chunk_size=500):
    """Splits text into clean non-empty chunks of given size."""
    chunks = [text[i:i+chunk_size].strip() for i in range(0, len(text), chunk_size)]
    chunks = [chunk for chunk in chunks if chunk]  # Remove empty
    print(f"✅ Total chunks created: {len(chunks)}")
    return chunks

def ingest_document(pdf_path):
    """Reads and embeds a PDF, saves FAISS index and chunk text."""
    os.makedirs(EMBEDDING_DIR, exist_ok=True)
    
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print("⚠️ Warning: No extractable text found in document.")
        return

    chunks = chunk_text(text)
    embeddings = MODEL.encode(chunks)
    
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(embeddings)
    faiss.write_index(index, os.path.join(EMBEDDING_DIR, "index.faiss"))

    with open(os.path.join(EMBEDDING_DIR, "chunks.txt"), "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

    print("✅ Document indexed and saved.")

def query_document(question, k=3):
    """Embeds the query and retrieves top-k matching chunks."""
    index_path = os.path.join(EMBEDDING_DIR, "index.faiss")
    chunks_path = os.path.join(EMBEDDING_DIR, "chunks.txt")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return "❌ No documents have been ingested yet."

    index = faiss.read_index(index_path)
    
    with open(chunks_path, encoding="utf-8") as f:
        chunks = f.readlines()

    question_embedding = MODEL.encode([question])
    D, I = index.search(question_embedding, k=k)

    print("🔍 Query:", question)
    print("📌 FAISS Distances:", D)
    print("📌 FAISS Indices:", I)

    results = []
    for idx in I[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx].strip())

    return "\n\n---\n\n".join(results) if results else "No relevant content found."
