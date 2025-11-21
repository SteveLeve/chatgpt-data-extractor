from chat_rag.query import setup_query_engine
from chat_rag.config import LLM_MODEL, LLM_PROVIDER

def test_chat():
    print(f"Testing RAG chat with Provider: {LLM_PROVIDER}, Model: {LLM_MODEL}...")
    
    # Setup query engine (handles model config internally)
    query_engine = setup_query_engine()
    
    # Test query
    query = "What conversations do I have?"
    print(f"\nQuery: {query}")
    print("\nGenerating response...")
    
    response = query_engine.query(query)
    
    print(f"\n{'='*60}")
    print("RESPONSE:")
    print(f"{'='*60}")
    print(response)
    print(f"{'='*60}\n")
    
    print("✓ SUCCESS: Chat interface is working!")

if __name__ == "__main__":
    test_chat()
