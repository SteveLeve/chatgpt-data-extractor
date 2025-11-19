# ADR 001: Technology Stack Selection

## Status
Proposed

## Context
We need to evolve a simple ChatGPT data extractor into a mature RAG pipeline. The system needs to:
- Run locally (preferred) but support APIs.
- Store structured conversation data.
- Store vector embeddings for retrieval.
- Provide a REPL interface and eventually a chatbot.
- Be containerized (Docker).

## Decision

We will use the following technology stack:

### 1. Language & Environment
- **Python 3.10+**: Existing codebase is Python, standard for AI/ML.
- **Docker & Docker Compose**: For managing dependencies (databases) and potentially the application itself.

### 2. Database (Structured & Vector)
- **PostgreSQL with pgvector**: 
    - **Rationale**: The user requested a SQL database for documents and a vector database for embeddings. Using PostgreSQL with the `pgvector` extension allows us to keep a single database instance for both structured metadata/content and vector embeddings. This simplifies the architecture and maintenance compared to managing a separate SQL DB and a dedicated Vector DB (like Chroma or Qdrant).
    - **Image**: `pgvector/pgvector:pg16`

### 3. RAG Framework / Orchestration
- **LlamaIndex**:
    - **Rationale**: LlamaIndex excels at data ingestion, indexing, and retrieval pipelines, which is the core of this request. It has strong support for "Node" management (keeping metadata with chunks), which aligns with the requirement to return original documents. It also supports swapping between local (Ollama/HuggingFace) and remote (OpenAI/Claude) models easily.

### 4. Local LLM & Embeddings
- **Inference Server**: **Ollama** (running in a separate container or on host).
    - **Rationale**: Standard for local LLM inference. Provides an OpenAI-compatible API.
- **Embeddings**: **HuggingFace (SentenceTransformers)** running locally via LlamaIndex.
    - **Model**: `BAAI/bge-m3` or `all-MiniLM-L6-v2` (configurable).
- **LLM**: **Llama 3** or **Mistral** (via Ollama).

### 5. Interface
- **Rich (Python Library)**: For building the initial REPL interface. It provides beautiful formatting for terminal output (markdown rendering, tables, etc.).

## Consequences
- **Positive**: Simplified infrastructure (one DB), powerful RAG capabilities out-of-the-box with LlamaIndex, flexible model switching.
- **Negative**: LlamaIndex has a learning curve and can be abstract; we must ensure we don't over-engineer the simple initial REPL.
