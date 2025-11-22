from typing import List, Optional
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import FunctionTool
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from chat_rag.storage import get_vector_store

def get_doc_content(doc_id: str) -> str:
    """
    Retrieves the full content of a document (conversation) by its ID.
    Use this when the user asks to see the "whole document", "full conversation", 
    or "source" for a specific item.
    
    Args:
        doc_id (str): The unique ID of the document to retrieve.
    """
    try:
        vector_store = get_vector_store()
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Create a retriever that filters by doc_id
        filters = MetadataFilters(
            filters=[ExactMatchFilter(key="id", value=doc_id)]
        )
        
        # Retrieve all nodes for this doc_id
        # We set similarity_top_k to a high number to ensure we get all chunks
        retriever = index.as_retriever(
            filters=filters, 
            similarity_top_k=100
        )
        
        nodes = retriever.retrieve("get all content")
        
        if not nodes:
            return f"No content found for document ID: {doc_id}"
            
        # Sort nodes by their position in the document to reconstruct order
        # Note: LlamaIndex nodes usually have relationships/metadata for order
        # For now, we'll assume the retriever returns them or we can sort if needed.
        # A simple concatenation might work if chunks are returned in order or have index.
        
        # Let's try to sort by node ID or just concatenate. 
        # Ideally, we should use the doc store, but we are using a vector store only setup.
        # Reconstructing from vector store nodes is a bit hacky but works for simple cases.
        
        # Sort by node id (usually doc_id_node_index)
        sorted_nodes = sorted(nodes, key=lambda x: x.node.node_id)
        
        full_text = "\n\n".join([node.text for node in sorted_nodes])
        return full_text
        
    except Exception as e:
        return f"Error retrieving document: {str(e)}"

def search_conversations(query: str) -> str:
    """
    Searches for conversations matching the query string.
    Use this to find relevant conversations, list items, or find specific topics.
    
    Args:
        query (str): The search query (e.g., "software engineer resume", "python error").
    """
    try:
        vector_store = get_vector_store()
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Use the standard retriever
        retriever = index.as_retriever(similarity_top_k=5)
        nodes = retriever.retrieve(query)
        
        if not nodes:
            return "No matching conversations found."
            
        results = []
        for i, node in enumerate(nodes, 1):
            title = node.metadata.get('title', 'Untitled')
            doc_id = node.metadata.get('id', 'Unknown ID')
            date = node.metadata.get('create_time', 'Unknown Date')
            preview = node.text[:200].replace('\n', ' ')
            
            results.append(f"{i}. TITLE: {title}\n   ID: {doc_id}\n   DATE: {date}\n   PREVIEW: {preview}...\n")
            
        return "\n".join(results)
        
    except Exception as e:
        return f"Error searching conversations: {str(e)}"

def get_rag_tools() -> List[FunctionTool]:
    """Returns a list of tools for the ReAct agent."""
    return [
        FunctionTool.from_defaults(fn=get_doc_content),
        FunctionTool.from_defaults(fn=search_conversations),
    ]
