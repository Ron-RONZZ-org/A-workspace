## Tool Calling Architecture for A-agento generi

### Decision

Add `chat()`, `supports_tools`, `ToolCall`, `LLMResponse` to A-core's LLMProvider.
Create `A_agento/tools.py` with encik search tools and orchestration loop.
Wire into `generi --formato enc`.

### Key principle
- `chat()` is separate from `generate()` — different contracts
- A-core provides transport, A-agento owns tool logic
- `generate()` wraps `chat()` for backward compat
- `supports_tools=False` by default; providers opt in

### Data flow
```
User: generi "macOS" --formato enc
  agento/tools.py:
    provider.chat(messages, tools=[search_encik, get_encik_entry])
    └── AI calls search_encik("macOS")
        └── agento executes: SELECT FROM encik_fts MATCH 'macOS'
        └── Returns: [Apple Inc., operaciumo, Unix, ...]
    └── AI calls get_encik_entry("uuid-of-apple")
        └── agento executes: SELECT * FROM encik WHERE uuid = ?
        └── Returns: full entry with ligilo, style, terminologio
    └── AI generates .enc with real UUIDs
```

### Files affected
- A-core: A/core/ai.py (~80 lines new)
- A-agento: tools.py (new, ~180 lines), commands/knowledge.py (~20 lines)

### Fallback
Providers without tool support (HuggingFace, Ollama <0.5): pre-search encik DB before generation and inject results as prompt context. Less dynamic but still functional.
