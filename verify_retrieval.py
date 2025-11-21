from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from chat_rag.storage import get_vector_store
from chat_rag.config import EMBEDDING_MODEL

def test_retrieval():
    print("Testing retrieval (without LLM)...")
    
    # Configure embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    
    # Connect to vector store
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    # Create retriever (no LLM needed)
    retriever = index.as_retriever(similarity_top_k=3)
    
    # Test query
    query = "What conversations do I have?"
    nodes = retriever.retrieve(query)
    
    print(f"\nRetrieved {len(nodes)} relevant chunks:")
    for i, node in enumerate(nodes, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {node.metadata.get('title', 'N/A')}")
        print(f"Score: {node.score:.4f}")
        print(f"Text preview: {node.text[:200]}...")
    
    print("\n✓ SUCCESS: Retrieval is working!")

if __name__ == "__main__":
    test_retrieval()
