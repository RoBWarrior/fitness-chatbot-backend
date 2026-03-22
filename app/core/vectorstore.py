import chromadb
from chromadb.config import Settings

chroma_client=chromadb.Client(Settings(persist_directory="chroma_store"))

def get_collection(name: str = "documents"):
    return chroma_client.get_or_create_collection(name)
