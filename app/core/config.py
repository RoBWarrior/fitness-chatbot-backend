from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAI_API_KEY = os.getenv("SERPAI_API_KEY")

# PostgreSQL Database Credentials
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print("🔑 GOOGLE_API_KEY:", GOOGLE_API_KEY[:5] if GOOGLE_API_KEY else "NOT FOUND")
# print("🔑 OPENAI_API_KEY:", OPENAI_API_KEY[:5] if OPENAI_API_KEY else "NOT FOUND")
print("🔑 SERPAI_API_KEY:", SERPAI_API_KEY[:5] if SERPAI_API_KEY else "NOT FOUND")
# print("Database URL:", DATABASE_URL)