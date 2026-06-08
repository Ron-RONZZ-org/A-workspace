# Tool-Calling Architecture for A-core LLM Providers

## Design Decision Log

### Problem
Adding tool-calling (function calling) support to A-core's LLM provider abstraction so that `agento generi "macOS" --formato enc` can search A-encik's database for related entries and use real UUIDs.

### Decision: New `chat()` method on `LLMProvider`

**Chosen:** Add `chat(messages, tools, **kwargs) -> LLMResponse` as a new method.

**Rejected options:**
- Adding `tools` parameter to existing `generate()`: incompatible return type (str vs str+tool_calls)
- Creating a separate `ToolLLMProvider` protocol: over-engineered

### Decision: Orchestration in A-agento, not A-core

**Chosen:** The tool execution loop and all tool definitions live in `A_agento/tools.py`.

**Rationale:** A-core provides the low-level `chat()` API only. Tool definitions (search_encik, get_encik_entry etc.) are domain-specific to A-encik. Keeping them in A-agento follows the existing pattern.

### Decision: Fallback via prompt injection

**Chosen:** When a provider doesn't support tools, pre-fetch encik results and inject them as context into the system prompt.

**Rationale:** `--formato enc` works with any provider, just better with tool-capable ones.

### Provider Tool Support

| Provider | Status | Method |
|----------|--------|--------|
| OpenAI | Native | `openai` library tools param |
| DeepSeek | Native | OpenAI-compatible, same lib |
| HuggingFace | Native | `InferenceClient.chat.completions()` supports `tools` |
| Ollama | Native (with /api/chat) | `/api/chat` endpoint, OpenAI-compatible tools format |

### Files Changed (minimal)

**A-core:**
- `A/core/ai.py` — Add `ToolCall`, `LLMResponse` dataclasses, `chat()` + `supports_tools` on all providers
- `A/__init__.py` — Export new types

**A-agento:**
- `A_agento/tools.py` — NEW: Tool definitions, execution handlers, orchestration loop, fallback
- `A_agento/commands/knowledge.py` — Add `--formato` option, call `generate_enc_entry()`
