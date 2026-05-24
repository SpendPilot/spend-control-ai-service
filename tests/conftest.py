from __future__ import annotations

import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://spendcontrol:spendcontrol@localhost:5432/spend_control",
)
os.environ.setdefault("JWT_SECRET_KEY", "dev-secret-change-me")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")
os.environ.setdefault("OLLAMA_MODEL", "llama3.2")
os.environ.setdefault("OLLAMA_REQUEST_TIMEOUT", "30")
