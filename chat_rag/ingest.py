import json
import hashlib
import datetime as dt
import html as html_mod
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from chat_rag.storage import get_storage_context
from chat_rag.config import EMBEDDING_MODEL

def _read_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def _extract_json_from_html(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding='utf-8', errors='replace')
    m = re.search(r"var\s+jsonData\s*=\s*(\[.*?\])\s*;", text, flags=re.DOTALL)
    if not m:
        raise ValueError("jsonData array not found in chat.html")
    json_blob = m.group(1)
    json_blob = html_mod.unescape(json_blob)
    return json.loads(json_blob)

def _collect_messages(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = conversation.get('mapping', {}) or {}
    messages: List[Dict[str, Any]] = []
    for node in mapping.values():
        msg = (node or {}).get('message')
        if msg:
            messages.append(msg)
    
    def key_fn(m: Dict[str, Any]):
        ct = m.get('create_time')
        return float(ct) if isinstance(ct, (int, float)) else float('inf')
    
    messages.sort(key=key_fn)
    return messages

def _render_conversation(conversation: Dict[str, Any]) -> str:
    messages = _collect_messages(conversation)
    lines = []
    for msg in messages:
        role = (msg.get('author') or {}).get('role')
        content = msg.get('content') or {}
        parts = content.get('parts') or []
        text = '\n'.join(str(p) for p in parts if p)
        if text.strip():
            lines.append(f"[{role}]: {text}")
    return "\n\n".join(lines)

def load_conversations(input_dir: Path) -> List[Dict[str, Any]]:
    json_path = input_dir / 'conversations.json'
    html_path = input_dir / 'chat.html'
    
    if json_path.exists():
        return _read_json(json_path)
    if html_path.exists():
        return _extract_json_from_html(html_path)
    raise FileNotFoundError("No conversations found in input directory")

def ingest_data(input_dir: Path, limit: Optional[int] = None, batch_size: int = 10):
    conversations = load_conversations(input_dir)
    
    if limit:
        conversations = conversations[:limit]
        print(f"Limiting to {limit} conversations.")
    
    print(f"Found {len(conversations)} conversations to process.")
    
    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.llm = None
    
    storage_context = get_storage_context()
    vector_store = storage_context.vector_store
    
    # Get existing index or create new one from vector store
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    total_batches = (len(conversations) + batch_size - 1) // batch_size
    
    for i in range(0, len(conversations), batch_size):
        batch = conversations[i : i + batch_size]
        print(f"Processing batch {i // batch_size + 1}/{total_batches} ({len(batch)} conversations)...")
        
        documents = []
        for conv in batch:
            text = _render_conversation(conv)
            if not text.strip():
                continue
                
            metadata = {
                "title": conv.get('title', 'Untitled'),
                "id": conv.get('id'),
                "create_time": conv.get('create_time'),
            }
            
            doc = Document(text=text, metadata=metadata)
            documents.append(doc)
            
        if documents:
            # Insert documents into the index (this generates embeddings and persists)
            # We use insert_nodes or refresh_ref_docs, but for simple ingestion:
            for doc in documents:
                index.insert(doc)
                
    print("Ingestion complete.")
