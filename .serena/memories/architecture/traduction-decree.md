# Traduki Feature — Architectural Decision (Revised)

**Date**: 2026-05-21
**Decision**: Implement as `agento traduki` (inside A-agento), NOT as standalone A-traduki module
**A-workspace issue**: #7 (repurposed as tracking)
**A-agento issue**: #56 (implementation tracking)

## Rationale

Translation is a direct user-to-LLM text operation. It belongs in A-agento as the general LLM interface alongside `generi`, reusing existing:
- I/O infrastructure (`_read_local_file`, `_save_to_file`, `_resolve_unique_path`)
- Provider config & prioritato fallback
- `-K/--konservi` and `-k/--kopii` flag conventions
- No A-core changes needed

## CLI

```
agento traduki <input> [-c <celo>] [-f <fonto>] [-K <output>] [-k] [-p <provider>]
```

- `-c/--celo` — target language (optional, default from config or auto-detect)
- `-f/--fonto` — source language (optional, default auto-detect)
- Both flags use Esperanto per AGENTS.md §1

Flat command (not grouped). Input auto-detects file vs string.

## Cross-Module Pattern

Other modules import `translate_text()` from A-agento directly. Never subprocess.

## AGENTS.md Impact

A-agento's scope expands from "email assistant" to "general LLM interface." AGENTS.md needs revision:
- Broadened purpose statement
- Updated architecture diagram (add commands/translation.py)
- Add `traduki` to command table
- Fix `.prompt` → `.md` in prompt documentation (currently says `.prompt` but all files and prompt_loader use `.md`)

## Prompt File

`src/A_agento/prompts/traduki.md` (not `.prompt` — convention is `.md` per prompt_loader.py)