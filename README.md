# ChatGPT Data Extractor & RAG Pipeline

A local-first tool to ingest, store, and interact with your chat history and documents from multiple sources (ChatGPT, Claude, Gemini, etc.) using RAG (Retrieval Augmented Generation).

**Goal:** Provide a self-contained and flexible environment for users to create their own knowledge bases from disparate sources.

## Features

- **Data Ingestion**: Parses ChatGPT `conversations.json` or `chat.html` exports.
- **Structured Storage**: Stores conversations in PostgreSQL.
- **Vector Search**: Uses `pgvector` for semantic search over conversation history.
- **Local RAG**: Runs entirely locally using Ollama (LLM) and HuggingFace (Embeddings), with support for external APIs.
- **REPL Interface**: Interactive command-line interface for chatting with your data.
- **Agentic RAG**: Uses a ReAct agent to intelligently search, filter, and retrieve full documents.
- **Smart Search**: Can find conversations by topic, not just semantic similarity.
- **Full Document Retrieval**: Can fetch the entire content of a conversation by ID.

## Prerequisites

- **Docker & Docker Compose**: For running the database.
- **Python 3.10+**: For running the application.
- **Ollama**: For local LLM inference (optional if using OpenAI API).

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd chatgpt-data-extractor
    ```

2.  **Start the Database**:
    ```bash
    docker-compose up -d
    ```

3.  **Create Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    Copy `.env.example` to `.env` and configure your settings:
    ```bash
    cp .env.example .env
    ```
    
    **For Anthropic Claude (Recommended for speed):**
    ```bash
    python setup_anthropic.py YOUR_ANTHROPIC_API_KEY
    ```
    
    Or manually edit `.env`:
    ```bash
    LLM_PROVIDER=anthropic
    LLM_MODEL=claude-haiku-4-5  # Fast and cost-effective
    ANTHROPIC_API_KEY=your-key-here
    ```
    
    **For local Ollama models:**
    ```bash
    LLM_PROVIDER=ollama
    LLM_MODEL=tinyllama:latest  # Fastest local model
    # or
    LLM_MODEL=llama3.1:8b  # Better quality (slower)
    ```

## Usage

### Ingest Data
Place your unzipped ChatGPT export in `source-data/` (or specify path).

**Test with a small subset first:**
```bash
python main.py ingest --input source-data --limit 10 --batch-size 5
```

**Ingest all data in batches:**
```bash
python main.py ingest --input source-data --batch-size 10
```

The batch processing approach allows you to:
- Test the pipeline quickly with `--limit`
- Process data incrementally (data is available immediately after each batch)
- Resume ingestion if interrupted

### Verify Retrieval (without LLM)
```bash
python scripts/verify_retrieval.py
```

### Chat (REPL)
Start the interactive chat session. The system will use the provider configured in your `.env` file (Anthropic or Ollama).

```bash
python main.py chat
```

### Reset Data
To clear all ingested data and start fresh (WARNING: This is destructive):

```bash
python scripts/reset_data.py
```

## Web Interface

The project includes a modern React-based web interface for chatting and managing data.

### 1. Build the Frontend
The frontend needs to be built once before it can be served by the backend.

```bash
cd frontend
npm install
npm run build
cd ..
```

### 2. Start the Server
Start the FastAPI backend, which also serves the built frontend.

```bash
python main.py serve
```

### 3. Access the UI
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## Architecture

See [docs/architecture](docs/architecture) for details.
- [ADR 001: Technology Stack](docs/architecture/ADR-001-tech-stack.md)
