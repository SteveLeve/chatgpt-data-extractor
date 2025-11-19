from llama_index.core import StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url
from chat_rag.config import DATABASE_URL

def get_vector_store() -> PGVectorStore:
    """
    Initialize and return the PGVectorStore.
    """
    url = make_url(DATABASE_URL)
    
    return PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="embeddings",
        embed_dim=1024,  # BGE-M3 dimension
    )

def get_storage_context() -> StorageContext:
    """
    Create a StorageContext with the Postgres vector store.
    """
    vector_store = get_vector_store()
    return StorageContext.from_defaults(vector_store=vector_store)
