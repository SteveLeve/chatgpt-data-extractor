import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import nest_asyncio
nest_asyncio.apply()
from llama_index.core.agent import FunctionAgent
from llama_index.llms.anthropic import Anthropic

async def main():
    # Use a dummy key, we expect an auth error or success, but NOT a loop error
    llm = Anthropic(api_key="sk-ant-dummy")
    agent = FunctionAgent(llm=llm, tools=[], system_prompt="Hi")
    print("Starting run...")
    try:
        response = await agent.run(user_msg="Hi")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
