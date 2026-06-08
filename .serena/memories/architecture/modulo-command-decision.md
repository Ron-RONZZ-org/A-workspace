# Architecture Decision: A modulo Command

## Date: 2026-05-03

## Context
Proposal to add `A modulo` command to A-core for module management (search, view, install, update, uninstall).

## Decision: Option A — Scope-limited enhancement

**Rejected**: Full `A modulo` with pip wrapping (Option B)
- No canonical registry on PyPI for A-modules
- Security escalation from scoped `_ensure_keyring()` to arbitrary package installs
- High maintenance: version conflicts, venv detection, permission handling
- Architecture boundary violation — A-core is a CLI framework, not a package manager
- `_ensure_keyring()` precedent does NOT generalize (scoped to one known package with user consent)

**Adopted**: Enhance `A list` + add static manifest for discovery (Option A)

### Components
| Component | Priority | Description |
|-----------|----------|-------------|
| `A list` with descriptions | P0 | Read from `importlib.metadata.metadata("A-{name}")` |
| `A modulo info {name}` | P0 | Show description, version, commands, URL, deps |
| `modules.json` manifest | P0 | Canonical list in A-core repo |
| `A modulo search` | P1 | Search manifest locally — no PyPI calls |
| `A modulo install {name}` | P2 | Guidance only — print `pip install` command |
| `A modulo update/uninstall` | No | `pip install --upgrade` / `pip uninstall` are sufficient |

### Design Constraints
1. Manifest at `A/core/modules.json` — versioned with A-core, updated by PR
2. Description priority: installed metadata > manifest fallback
3. No PyPI API calls at runtime
4. No pip subprocess (except existing `_ensure_keyring()` — unchanged)
5. Degrade gracefully if manifest is stale

### Rationale
- Real UX gap is discovery + description, not installation mechanics
- `pip install A-tempo` is already one command; the pain is not knowing options
- Manifest is cheap to maintain (9 modules, updated rarely)
- Keeps A-core within its defined scope as a CLI framework
