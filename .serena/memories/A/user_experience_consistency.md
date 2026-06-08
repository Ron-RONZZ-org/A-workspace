# A User Experience Consistency with autish-legacy

## Principle

All A- modules (A-vorto, A-encik, etc.) must maintain **feature parity and command compatibility** with autish-legacy for user experience continuity.

## Why

Users migrating from autish-legacy to A expect:
- Same command names and aliases
- Same arguments and options
- Same output format
- Same data paths or proper migration

## Implementation Rule

Before adding new CLI commands or changing existing ones:
1. **Check autish-legacy** for the equivalent command
2. **Match the command signature exactly** - same args, same options
3. **Only add A-specific features** when autish-legacy doesn't have them

## Command Registration

Module grouping commands (e.g., `A lien`, `A organizi`) must NOT be registered as
top-level entry points. Only leaf commands (e.g., `A retposto`, `A kontakto`,
`A kalendaro`, `A todo`, `A taglibro`) should be registered directly.

## Command Mapping

### vorto
| autish-legacy | A | Notes |
|--------------|---|------|
| `aldoni` | `aldoni` | ✓ exact match |
| `vidi` | `vidi` | ✓ exact match |
| `modifi` | `modifi` | ✓ exact match |
| `serci` | `serci` | ✓ exact match |
| `forigi` | `forigi` | ✓ exact match |
| `malfari` | `malfari` | ✓ exact match |
| `eksporti` | `eksporti` | ✓ exact match |
| `importi` | `importi` | ✓ exact match |

### encik
| autish-legacy | A | Notes |
|--------------|---|------|
| `agordi` | `agordi` | ✓ |
| `aldoni` | `aldoni` | ✓ |
| `modifi` | `modifi` | ✓ |
| `vidi` | `vidi` | ✓ |
| `eksporti` | `eksporti` | ✓ |
| `generi` | `generi` | ✓ |
| `semantika-serci` | `semantika-serci` | ✓ |
| `serci` | `serci` | ✓ |
| `ls` | `ls` | ✓ |
| `forigi` | `forigi` | ✓ |

## Data Paths

- autish-legacy: `~/.local/share/autish/vorto.db`, `~/.local/share/autish/encik.db`
- A: `~/.local/share/A/vorto.db`, `~/.local/share/A/encik.db`

Migration tools must handle path changes.

## Implementation Status

### A-vorto ✓ (commit 80f51d3 → d24b577)
- Full command signature parity with autish-legacy
- Uses `A.utils.copy_to_clipboard` for clipboard

### A-encik ✓ (commit b242934)
- Added clipboard options to aldoni/modifi/vidi/serci
- Added advanced filter aliases to serci

### A-lien ✓ (commit bf53bb3)
- Removed `lien` top-level command — use `A retposto` / `A kontakto` directly
- Contact migration: only verified contacts (`konfirmita = 1`)
- Added email account migration + keyring password migration

### A-organizi ✓ (commit 5e4f3b2)
- Removed `organizi` top-level command — use `A kalendaro` / `A todo` / `A taglibro` directly
