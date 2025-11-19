# AGENTS.md

## Context
This project is a RAG (Retrieval Augmented Generation) pipeline for personal ChatGPT data. It prioritizes local execution and privacy.

## Tech Stack
- **Language**: Python 3.10+
- **Database**: PostgreSQL 16 with `pgvector` extension.
- **RAG Framework**: LlamaIndex.
- **LLM**: Ollama (Local) or OpenAI (API).
- **Embeddings**: HuggingFace `BAAI/bge-m3` (Local).
- **CLI**: `argparse` + `rich`.

## Project Structure
- `chat_rag/`: Main package.
    - `ingest.py`: ETL logic (Parsing -> Embedding -> DB).
    - `storage.py`: DB connection and vector store setup.
    - `query.py`: Retrieval and generation logic.
    - `interface.py`: UI/REPL.
    - `config.py`: Configuration loading.
- `main.py`: CLI entry point.
- `docker-compose.yml`: Infrastructure (Postgres).

## Conventions
- **Type Hinting**: Strict type hints required.
- **Docstrings**: Google style docstrings.
- **Path Handling**: Use `pathlib.Path` instead of `os.path`.
- **Async**: Use `asyncio` where appropriate for I/O bound tasks (DB, API calls).
