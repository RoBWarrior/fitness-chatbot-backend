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

# --- API KEYS ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Providers Setup ---
client = None
gemini_ready = False

if OPENAI_API_KEY and OpenAI:
    client = OpenAI(api_key=OPENAI_API_KEY)
    PROVIDER = "openai"

elif GOOGLE_API_KEY and genai:
    genai.configure(api_key=GOOGLE_API_KEY)
    PROVIDER = "gemini"
    gemini_ready = True

else:
    raise ImportError("❌ No embedding provider available. Provide OPENAI_API_KEY or GOOGLE_API_KEY.")

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

    except Exception as e:
        print(f"❌ {PROVIDER} embedding error: {e}")
        return []

print(f"✅ Embedding provider initialized: {PROVIDER}")
