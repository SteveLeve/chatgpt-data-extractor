import asyncio
# import nest_asyncio
# nest_asyncio.apply()

from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from chat_rag.storage import get_vector_store
from chat_rag.config import EMBEDDING_MODEL, LLM_MODEL, LLM_PROVIDER, ANTHROPIC_API_KEY
from chat_rag.tools import get_rag_tools

SYSTEM_PROMPT = """
You are a helpful AI assistant for exploring a user's ChatGPT conversation history.
You have access to tools to search conversations and retrieve full document contents.

GUIDELINES:
1. **Search First**: When asked about a topic, use `search_conversations` to find relevant items.
2. **Full Content**: If the user asks to see a "whole conversation", "full text", or "source", use `get_doc_content` with the specific ID found from search.
3. **Citations**: Always cite the Title and ID of conversations you reference.
4. **Follow-up Questions**: At the very end of your response, ALWAYS provide 1-3 relevant follow-up questions to help the user explore further. Format them as a numbered list.

Example Follow-ups:
1. Would you like to see the full content of the "Resume Review" conversation?
2. Should we search for other conversations about "Python"?
3. Do you want to summarize the key points from this thread?
"""

def setup_agent():
    # Setup Embedding Model
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    
    # Setup LLM based on provider
    if LLM_PROVIDER == "anthropic":
        Settings.llm = Anthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY)
        AgentClass = FunctionAgent
    else:  # ollama
        Settings.llm = Ollama(model=LLM_MODEL, request_timeout=600.0)
        AgentClass = ReActAgent
    
    # Get Tools
    tools = get_rag_tools()
    
    # Create Agent (Workflow)
    agent = AgentClass(
        llm=Settings.llm, 
        tools=tools, 
        system_prompt=SYSTEM_PROMPT
    )
    
    return agent

async def query_async(question: str, agent=None):
    if agent is None:
        agent = setup_agent()
    return await agent.run(user_msg=question)

def query(question: str):
    return asyncio.run(query_async(question))
