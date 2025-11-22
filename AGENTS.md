# AGENTS.md

## Context
This project is a RAG (Retrieval Augmented Generation) pipeline for personal ChatGPT data. It prioritizes local execution and privacy.

## Tech Stack
- **Language**: Python 3.10+
- **Database**: PostgreSQL 16 with `pgvector` extension.
- **RAG Framework**: LlamaIndex (Agentic RAG with Workflows).
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
- **Documentation Sync**: **CRITICAL** - Always update documentation when making functional changes:
  - Update `README.md` for user-facing changes (new features, setup steps, configuration)
  - Update `AGENTS.md` for developer/agent-facing changes (architecture, conventions, tech stack)
  - Update ADRs in `docs/architecture/` when making technology choices
  - Update `.env.example` when adding new configuration options
  - Keep code comments in sync with implementation

## Current Configuration
- **LLM Provider**: Anthropic (configurable via `.env`)
- **Default Model**: `claude-haiku-4-5` (fast, cost-effective)
- **Fallback**: Local Ollama models supported
- **Embedding Model**: `BAAI/bge-m3` (local, 1024 dimensions)
