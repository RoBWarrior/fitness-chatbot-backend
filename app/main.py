import os
import sys

# SQLite workaround for ChromaDB on platforms with outdated sqlite3 (like Render)
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import json
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, upload, workflow, query, chat, auth

app = FastAPI(title="Workflow Builder Backend")

from app.core.db import create_tables

@app.on_event("startup")
async def startup_event():
    create_tables()

# Allow CORS for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (update this to your Vercel URL later for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/config")
async def get_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "persona.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(workflow.router, prefix="/workflow", tags=["Workflow"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])