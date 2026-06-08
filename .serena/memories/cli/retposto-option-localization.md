# Retposto CLI Option Localization (Issue #22)

## What changed

Removed 4 deprecated legacy compatibility aliases from `retposto.py`:
- `retposto ls` (use `retposto konton ls`)
- `retposto vidi` (shadowed email viewer; use `retposto konton vidi` for accounts)
- `retposto aldoni-konton` (use `retposto konton aldoni`)
- `retposto forigi-konton` (use `retposto konton forigi`)

All hidden, but `retposto vidi` alias **overwrote** the real email viewer `retposto_vidi_mesago`
because Typer/Click stores commands in an OrderedDict by name — second registration wins.

## Localization policy

**English (kept as-is):** `--from`, `--to`, `--cc`, `--bcc`, `--subject`, `--body`
These are standard email field names understood universally.

**Esperanto (localized):**
| Old | New | Commands affected |
|-----|-----|------------------|
| `--account` | `--konto` | preni, sendi, dosierujoj, mesagxoj, serci |
| `--attach` | `--alglui` | sendi |
| `--folder` | `--dosierujo` | mesagxoj |
| `--limit` | `--limo` | mesagxoj, serci |
| `--after` | `--post` | serci |
| `--before` | `--antaux` | serci |
| `--read` | `--legita` | serci |
| `--unread` | `--nelegita` | serci |
| `--priority` | `--prioritato` | serci |

Short flags (`-a`, `-f`, `-l`, `-p`) preserved where they didn't conflict.

## Breaking changes

Any scripts using the old option names on retposto commands will break.
