from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from chat_rag.storage import get_vector_store
from chat_rag.config import LLM_MODEL, EMBEDDING_MODEL

def setup_query_engine():
    # Setup Models
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=300.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    
    # Connect to Vector Store
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    return index.as_query_engine()

def query(question: str):
    query_engine = setup_query_engine()
    response = query_engine.query(question)
    return response
