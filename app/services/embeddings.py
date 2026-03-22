import os

# Try OpenAI first
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Try Gemini second
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Try local embeddings fallback
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

# --- API KEYS ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Providers Setup ---
client = None
gemini_ready = False
local_model = None

if OPENAI_API_KEY and OpenAI:
    client = OpenAI(api_key=OPENAI_API_KEY)
    PROVIDER = "openai"

elif GOOGLE_API_KEY and genai:
    genai.configure(api_key=GOOGLE_API_KEY)
    PROVIDER = "gemini"
    gemini_ready = True

elif SentenceTransformer:
    try:
        local_model = SentenceTransformer("all-MiniLM-L6-v2")
        PROVIDER = "local"
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load local embedding model: {e}")

else:
    raise ImportError("❌ No embedding provider available. Install OpenAI, Gemini, or sentence-transformers.")

# --- Unified Function ---
def get_embedding(text: str) -> list[float]:
    global PROVIDER
    try:
        if PROVIDER == "openai":
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding

        elif PROVIDER == "gemini":
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            return response.embedding if hasattr(response, "embedding") else response["embedding"]

        elif PROVIDER == "local":
            embedding = local_model.encode(text)
            # make sure it's converted properly
            if hasattr(embedding, "tolist"):
                embedding = embedding.tolist()
                
            print(len(embedding))
            return embedding

    except Exception as e:
        print(f"❌ {PROVIDER} embedding error: {e}")
        return []

print(f"✅ Embedding provider initialized: {PROVIDER}")
