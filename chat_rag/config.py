import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DATA_DIR = BASE_DIR / "source-data"
CONVERSATIONS_DIR = BASE_DIR / "conversations"

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password@localhost:5432/chatgpt_rag"
)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "anthropic"
LLM_MODEL = os.getenv("LLM_MODEL", "tinyllama:latest")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
