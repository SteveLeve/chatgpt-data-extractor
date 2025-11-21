from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from chat_rag.storage import get_vector_store
from chat_rag.config import EMBEDDING_MODEL, LLM_MODEL

def test_chat():
    print(f"Testing RAG chat with model: {LLM_MODEL}...")
    
    # Configure models
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=300.0)
    
    # Connect to vector store
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    # Create query engine
    query_engine = index.as_query_engine()
    
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
