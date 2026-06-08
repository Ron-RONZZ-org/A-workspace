# Provider State Split: A-core → A-agento

## Decision
`ai.py` in A-core was split: factory + key storage stayed in core; default provider list, auto-detection, and env var checkers moved to A-agento `provider_state.py`.

## Rationale
The default provider list and fallback logic are application state owned by A-agento. A-core should only hold the protocol (providers.py) + factory (get_provider) + keyring wrappers (save_api_key). Having the default list in core created an implicit coupling where A-agento wrote state that A-core read.

## New Architecture

### A-core keeps
- `providers.py` — LLMProvider protocol, ToolCall, LLMResponse, OpenAICompatibleProvider, OllamaProvider
- `ai.py` (107 lines) — get_provider(provider_type, **kwargs), save_api_key, get_api_key only. No defaults, no auto-detection, no env loading.

### A-agento gets
- `provider_state.py` — get_fallback_order(), get_provider_with_fallback()
- `provider_config.py` — prioritato column (INTEGER, lower = higher priority), auto-assigns newest = 0
- `_helpers.py:get_provider_or_exit(None)` — uses get_provider_with_fallback()
- `agordo.py` — `--prioritato/-p` on aldoni, prioritato column in ls, default sets prioritato=0
- `agordo_crud.py` — `--prioritato/-p` on modifi, prioritato row in vidi

### Fallback Order
When no `--provizanto` specified:
1. Query DB: `SELECT * FROM provizanto_agordoj ORDER BY prioritato ASC, kreita_je DESC`
2. For each unique provider type, check `_resolve_api_key(pt)` from A.core.providers
3. First type with an available key → create provider
4. If none available → error with list of configured types

### Prioritato Auto-Assignment
- New entry without `--prioritato` → shifts existing +1, new gets 0 (= highest priority, tried first)
- "Newest first" is the default behavior
- `agordi default <provider>` sets prioritato=0 for that provider
- `agordi modifi <provider> --prioritato N` for explicit reordering
