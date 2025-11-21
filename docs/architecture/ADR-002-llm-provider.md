# ADR 002: LLM Provider Selection - Anthropic Claude

## Status
Accepted

## Context
The initial plan was to use local LLM inference via Ollama. During implementation and testing, we encountered significant performance issues:
- **tinyllama:latest** (0.6GB): Timed out after 300+ seconds
- **llama3.2:3b-instruct-q4_K_S** (1.8GB): Required 57.8GB system memory (error), only 9.5GB available
- **Hardware constraints**: Local models are too slow on the available CPU-only hardware

The user requires a responsive chat interface for exploring their conversation history via RAG.

## Decision

We will use **Anthropic Claude Haiku** (`claude-haiku-4-5`) as the primary LLM provider while maintaining support for local Ollama models as a fallback option.

### Implementation Details:
- **Primary**: Anthropic Claude Haiku API
- **Fallback**: Ollama local models (configurable via `.env`)
- **Configuration**: `LLM_PROVIDER` environment variable switches between `anthropic` and `ollama`

## Consequences

### Positive:
- **Fast response times**: API-based inference is significantly faster than local CPU inference
- **Cost-effective**: Claude Haiku is one of the most cost-effective API options
- **Reliability**: No hardware resource constraints
- **Flexibility**: System supports both API and local models via configuration

### Negative:
- **API dependency**: Requires internet connection and valid API key
- **Cost**: Per-token pricing (though minimal with Haiku)
- **Privacy**: Data sent to external API (conversation chunks sent for RAG retrieval)

### Mitigation:
- Local Ollama support maintained for offline/private use cases
- User can switch providers by changing `.env` configuration
- Only retrieval chunks are sent to the API, not full conversation history
