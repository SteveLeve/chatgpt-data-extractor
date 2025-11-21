from sqlalchemy import create_engine, text
from chat_rag.config import DATABASE_URL

def check_db():
    # Force sync driver for this check
    url = DATABASE_URL.replace("+asyncpg", "+psycopg2")
    engine = create_engine(url)
    with engine.connect() as conn:
        try:
            # Try configured table name first
            result = conn.execute(text("SELECT count(*) FROM embeddings"))
            print(f"Embeddings count: {result.scalar()}")
        except Exception as e:
            print(f"Error querying 'embeddings': {e}")
            conn.rollback()
            # Try default LlamaIndex table name
            try:
                result = conn.execute(text("SELECT count(*) FROM data_embeddings"))
                print(f"Embeddings count: {result.scalar()}")
            except Exception as e2:
                print(f"Error querying 'data_embeddings': {e2}")

if __name__ == "__main__":
    check_db()
