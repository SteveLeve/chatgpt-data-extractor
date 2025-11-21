#!/usr/bin/env python3
"""
Helper script to configure .env file for Anthropic Claude.
Updates the .env file with Anthropic settings.
"""
import sys

def setup_anthropic_env(api_key: str):
    """Update .env file with Anthropic configuration."""
    env_content = f"""DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/chatgpt_rag
LLM_PROVIDER=anthropic
LLM_MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY={api_key}
EMBEDDING_MODEL=BAAI/bge-m3
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ .env file updated with Anthropic Claude Haiku configuration")
    print(f"✓ Model: claude-haiku-4-5")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_anthropic.py YOUR_API_KEY")
        sys.exit(1)
    
    api_key = sys.argv[1]
    setup_anthropic_env(api_key)
