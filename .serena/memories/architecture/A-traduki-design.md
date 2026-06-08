# A-traduki Module - Architectural Decision

**Status**: Approved, not yet implemented
**Issue**: https://github.com/Ron-RONZZ-org/A-workspace/issues/7
**Date**: 2026-05-21

## Summary

New A-module for text translation via CLI. Single-command design, LLM-based backend reusing `A.core.ai.get_provider()`.

## CLI

```
a traduki <input> -t <target_lang> [-s <source_lang>] [-K <output_path>] [-k]
```

- `-K/--konservi` — output filepath (convention from A-agento)
- `-k/--kopii` — copy to clipboard
- Input auto-detection: file if Path(input).exists(), else raw string

## Architecture

Stateless MVP (no SQLite). Provider abstraction in `providers.py`. Config via ConfigSchema at `~/.config/A/A-traduki/config.toml`.

## Flags

- `-K/--konservi` (capital K to distinguish from `-k/--kopii` for clipboard)
- `-k/--kopii`
- `-t/--target`
- `-s/--source`
- `-p/--provider`

## Implementation Phases

See issue #7 for full plan.
