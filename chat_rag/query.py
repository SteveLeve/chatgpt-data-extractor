from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from chat_rag.storage import get_vector_store
from chat_rag.config import EMBEDDING_MODEL, LLM_MODEL, LLM_PROVIDER, ANTHROPIC_API_KEY

def setup_query_engine():
    # Setup Embedding Model
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    
    # Setup LLM based on provider
    if LLM_PROVIDER == "anthropic":
        Settings.llm = Anthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY)
    else:  # ollama
        Settings.llm = Ollama(model=LLM_MODEL, request_timeout=600.0)
    
    # Connect to Vector Store
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    return index.as_query_engine(similarity_top_k=2)

def query(question: str):
    query_engine = setup_query_engine()
    response = query_engine.query(question)
    return response
