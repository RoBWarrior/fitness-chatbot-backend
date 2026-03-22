from fastapi import APIRouter, UploadFile, File, Form
import uuid
import tempfile

from app.services.extractor import extract_text_from_pdf
from app.services.embeddings import get_embedding
from app.services.retriever import store_document, delete_document
from app.services.db_helpers import save_document_record, get_user_documents, delete_document_record

router = APIRouter()

@router.post("/")
async def upload_file(user_id: int = Form(...), file: UploadFile = File(...)):
    try:
    # Save temp file
        temp_path = tempfile.NamedTemporaryFile(delete=False).name
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        text = extract_text_from_pdf(temp_path)

        # Generate embeddings
        embedding = get_embedding(text)

        # Store in ChromaDB with user_id metadata
        doc_id = store_document(text, embedding, user_id)
        
        # Save record in Postgres
        save_document_record(doc_id, user_id, file.filename)

        return {"status": "success", "doc_id": doc_id, "text_length": len(text)}
    
    except Exception as e:
        print(f"An error occured during uploading {e}")
