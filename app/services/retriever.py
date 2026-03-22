# services/retriever.py
import uuid
from app.services.embeddings import get_embedding
from app.core.vectorstore import get_collection

def store_document(text: str, embedding: list[float], user_id: int):
    try:
        # embedding = get_embedding(text)
        # if not embedding:  # empty or None
        #     raise ValueError("Embedding generation failed. Check API key.")
        doc_id = str(uuid.uuid4())
        collection = get_collection()
        collection.add(documents=[text], embeddings=[embedding], ids=[doc_id], metadatas=[{"user_id": user_id}])
        return doc_id
    except Exception as e:
        print(f"An error occured while storing the document {e}")

def query_similar(query: str, user_id: int, top_k: int = 3):
    try:
        query_embedding = get_embedding(query)
        if not query_embedding:
            print("⚠️ Skipping vector search because embedding failed.")
            return []
            
        collection = get_collection()
        results = collection.query(
            query_embeddings=[query_embedding], 
            n_results=top_k,
            where={"user_id": user_id}
        )
        
        docs = results.get("documents", [])
        if docs and isinstance(docs[0], list):
            docs = docs[0]
            
        return docs
    except Exception as e:
        print(f"An error occured while fetching the query with the document {e}")
        return []

def delete_document(doc_id: str):
    try:
        collection = get_collection()
        collection.delete(ids=[doc_id])
        return True
    except Exception as e:
        print(f"An error occurred while deleting document from vectorstore {e}")
        return False
