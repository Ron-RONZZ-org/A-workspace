# A-agento Design Document

## Module Overview

A-agento provides AI-powered email assistance for the A ecosystem, leveraging LLM providers (OpenAI, Ollama) for summarization, smart reply generation, and action extraction from emails.

## Architecture

### Directory Structure
```
A-agento/
├── src/A_agento/
│   ├── __init__.py        # exports: app
│   ├── cli.py           # Typer app with commands
│   ├── service.py       # AgentService orchestration
│   ├── prompts.py      # Prompt templates
│   └── data/
│       └── storage.py  # SQLite for agent metadata
├── tests/
├── pyproject.toml
└── AGENTS.md
```

### Cross-Module Dependencies

A-agento coordinates between:
- **A-core.ai**: LLM provider abstraction (OpenAI, Ollama)
- **A-lien**: Email access (RetpostoService for messages, contacts)
- **A-organizi**: Calendar events (EventService), todos (TodoService)
- **A-encik**: Knowledge entries (EncikService)

All cross-module imports use **runtime detection** — modules are optional until explicitly used.

## LLM Provider Abstraction (A-core)

### Protocol Design
```python
class LLMProvider(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...
    async def generate_async(self, prompt: str, **kwargs) -> str: ...
    @property
    def name(self) -> str: ...
```

### Provider Types
1. **OpenAIProvider**: Uses `openai` library, API key from keyring (`A-core/{profile}/openai_key`)
2. **OllamaProvider**: Uses `requests` to hit local Ollama API (`http://localhost:11434/api/generate`)

### Factory Function
- `get_provider(provider_type: str, **kwargs) -> LLMProvider`
- `save_api_key()`, `get_api_key()`, `set_default_provider()`

## Security Considerations

1. **API key storage**: OpenAI key stored in system keyring, never in SQLite
2. **Confirmation gate**: All AI-suggested write actions require user confirmation (never auto-execute)
3. **Privacy**: User chooses provider; Ollama = fully local, no data leaves machine
4. **Input validation**: Sanitize prompts before sending to LLM

## Implementation Phases

### Phase 1: A-core.ai Foundation
- Abstract `LLMProvider` protocol in A-core
- OpenAI and Ollama implementations
- Keyring integration for API key
- Factory function

### Phase 2: A-agento Read-Only Features
- Email summarization (read emails via A-lien, summarize via LLM)
- Smart reply draft generation (read context, generate draft)
- Action extraction (parse email → suggest calendar/todo/encik entry)

### Phase 3: Write Actions (with Confirmation)
- Create calendar event from email
- Create todo from email
- Save to encik knowledge base
- All require explicit user confirmation

## Confirmation Gate Pattern
```python
def _confirm_action(description: str) -> bool:
    """Show action preview and ask user to confirm."""
    info(f"Proponita ago: {description}")
    result = typer.confirm(tr_multi("Ĉu plenumi?", "Execute?", "Exécuter?"))
    if not result:
        info(tr("Nuligita."))
        return False
    return True
```

## Email Summarization Flow
1. User runs `agento resumu`
2. AgentService fetches recent unread emails via A-lien RetpostoService
3. Each email passed to LLM with summarization prompt
4. Results displayed as numbered list with action options

## Key Design Decisions

1. **Provider abstraction**: Both cloud (OpenAI) and local (Ollama) via protocol
2. **Scope**: Read-only first (summarization), then write with confirmation
3. **Confirmation**: Never auto-execute AI-suggested writes
4. **Privacy**: User opt-in for cloud; local Ollama is default for privacy
5. **Runtime detection**: Cross-module imports graceful when modules unavailable