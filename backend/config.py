"""
CrimeNet AI - Configuration Settings
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "backend_storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
VECTOR_INDEX_DIR = STORAGE_DIR / "vector_indices"
AUDIT_LOG_PATH = STORAGE_DIR / "audit_ledger.jsonl"
CASES_METADATA_PATH = STORAGE_DIR / "cases_metadata.json"

for d in [STORAGE_DIR, UPLOADS_DIR, VECTOR_INDEX_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API Keys & LLM settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "offline")  # "openai", "gemini", or "offline"

# RAG & Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
SIMILARITY_TOP_K = int(os.getenv("SIMILARITY_TOP_K", "4"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.05"))

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "*",
]
