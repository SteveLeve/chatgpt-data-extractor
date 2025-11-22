import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
from chat_rag.config import ANTHROPIC_API_KEY, LLM_MODEL

async def test_agent():
    llm = Anthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY)
    agent = FunctionAgent(llm=llm, tools=[], system_prompt="You are a helpful assistant.")
    
    print("Running agent...")
    response = await agent.run(user_msg="Hello, who are you?")
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_agent())
