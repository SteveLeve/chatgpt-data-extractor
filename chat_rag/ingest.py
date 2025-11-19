import json
import hashlib
import datetime as dt
import html as html_mod
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from llama_index.core import Document, VectorStoreIndex
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

def ingest_data(input_dir: Path):
    conversations = load_conversations(input_dir)
    documents = []
    
    print(f"Found {len(conversations)} conversations. Processing...")
    
    for conv in conversations:
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
    
    print(f"Created {len(documents)} documents. Indexing...")
    
    storage_context = get_storage_context()
    
    # Initialize index (this will generate embeddings and store in PG)
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    print("Ingestion complete.")
