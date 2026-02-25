from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from pinecone_init import PineconeClient
from config import PORT, API_KEY
from pydantic import BaseModel
from process import extract_text_from_pdf, split_text
from agent.agent import get_agent_response
import uvicorn
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Syllabus Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pinecone = PineconeClient()

class UserQuery(BaseModel):
    namespace: str
    query: str

async def verify_api_key(api_key: str = Header(..., alias="api-key")):
    if (api_key != API_KEY):
        raise HTTPException(status_code = 401, detail = "Wrong API key")

    return api_key

@app.get("/")
async def root():
    return {
        "message": "Syllabus Chatbot API"
    }

@app.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_syllabus(file: UploadFile, namespace: str):
    """Upload syllabus PDF"""
        
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files currently allowed")
    
    # Check if syllabus already uploaded
    if namespace in pinecone.list_namespaces():
        return {
            "status": "error",
            "namespace": namespace,
            "message": "Syllabus already uploaded"
        }

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Process the text and upload to Pinecone
        text = extract_text_from_pdf(tmp_path)
        chunks = split_text(text)
        pinecone.upload_chunks(chunks, namespace)
        
        return {
            "status": "success",
            "namespace": namespace,
            "chunks": len(chunks)
        }
    finally:
        os.unlink(tmp_path)

@app.post("/ask", dependencies=[Depends(verify_api_key)])
async def ask_question(request: UserQuery):
    """Ask a question about uploaded syllabus"""

    if request.namespace not in pinecone.list_namespaces():
        raise HTTPException(status_code=404, detail="Syllabus not found")

    # Answer each user question using stored Pinecone & agent response
    vector_store = pinecone.get_vectorstore(request.namespace)
    answer = await get_agent_response(vector_store, request.query)

    return {
        "namespace": request.namespace,
        "question": request.query,
        "answer": answer
    }

@app.get("/syllabi")
async def list_syllabi():
    """List all uploaded syllabi"""

    namespaces = pinecone.list_namespaces()
    return {
        "syllabi": namespaces,
        "count": len(namespaces)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
