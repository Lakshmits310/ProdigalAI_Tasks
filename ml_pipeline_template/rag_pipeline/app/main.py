from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from vector_store import ingest_document, query_document

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RAG API is up!"}

@app.post("/upload_doc")
async def upload_doc(file: UploadFile = File(...)):
    path = f"../docs/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    ingest_document(path)
    return {"status": "Document uploaded and ingested"}

@app.get("/query")
def query(q: str):
    response = query_document(q)
    return JSONResponse({"response": response})

@app.get("/health")
def health():
    return {"status": "healthy"}
