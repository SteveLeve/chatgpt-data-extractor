from chat_rag.query import query
import sys

def test_query():
    print("Testing RAG retrieval...")
    response = query("What conversations do I have?")
    print(f"Response: {response}")
    
    if not response:
        print("FAILED: No response received")
        sys.exit(1)
    print("SUCCESS: Retrieval worked")

if __name__ == "__main__":
    test_query()
