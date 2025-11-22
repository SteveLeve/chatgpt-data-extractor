import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_rag.query import query
from chat_rag.config import LLM_MODEL, LLM_PROVIDER

def test_chat():
    print(f"Testing Agentic RAG with Provider: {LLM_PROVIDER}, Model: {LLM_MODEL}...")
    
    # Test query that should trigger get_doc_content
    q = "Get the full content of the document with ID 68ee7acd-1f6c-8326-bbcd-5fd88adf140c"
    print(f"\nQuery: {q}")
    print("\nGenerating response (expecting tool use)...")
    
    # Use the query function which handles agent setup and async execution
    response = query(q)
    
    print(f"\n{'='*60}")
    print("RESPONSE:")
    print(f"{'='*60}")
    print(response)
    print(f"{'='*60}\n")
    
    print("✓ SUCCESS: Agent interface is working!")

if __name__ == "__main__":
    test_chat()
