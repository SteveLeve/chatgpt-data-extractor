# Product Roadmap

This document outlines the planned improvements and features for the ChatGPT Data Extractor.

## 1. LLM Provider Flexibility
Goal: Enable users to pick their LLM of choice and convenience while keeping data ingestion local and private.

- **[Issue #1](https://github.com/SteveLeve/chatgpt-data-extractor/issues/1): Support OpenAI API Keys and Models**
  - Allow users to use OpenAI models if they lack local GPU capacity.
- **[Issue #2](https://github.com/SteveLeve/chatgpt-data-extractor/issues/2): Support Ollama Cloud Models**
  - Support connecting to remote Ollama instances with API keys.
- **[Issue #3](https://github.com/SteveLeve/chatgpt-data-extractor/issues/3): Support Claude Desktop via MCP**
  - Integrate with local Claude Desktop for inference.

## 2. Non-LLM Search & Retrieval
Goal: Enhance discovery with traditional search methods and better context.

- **[Issue #4](https://github.com/SteveLeve/chatgpt-data-extractor/issues/4): Enhance Document Retrieval Tools**
  - Add keyword search and fuzzy matching.
- **[Issue #5](https://github.com/SteveLeve/chatgpt-data-extractor/issues/5): Include Links to Full Documents in Chat**
  - Provide direct links to source documents in chat responses.

## 3. Ingestion Workflows
Goal: Centralize disparate conversations from multiple providers.

- **[Issue #6](https://github.com/SteveLeve/chatgpt-data-extractor/issues/6): Multi-Provider Ingestion Support**
  - Add support for ingesting data from other AI chat providers.

## 4. Tagging Feature
Goal: Improve search and exploration efficiency with thematic tags.

- **[Issue #7](https://github.com/SteveLeve/chatgpt-data-extractor/issues/7): Thematic Tagging System**
  - Extract thematic tags from documents and chunks.
- **[Issue #8](https://github.com/SteveLeve/chatgpt-data-extractor/issues/8): Managed Tag Lookup Table**
  - Manage tags in a structured lookup table for efficiency.

## 5. Optimization & Maintenance
Goal: Ensure the system is efficient and avoids redundant work.

- **[Issue #9](https://github.com/SteveLeve/chatgpt-data-extractor/issues/9): De-duplication & Content Refresh**
  - Smartly handle bulk exports to avoid re-processing unchanged conversations.
