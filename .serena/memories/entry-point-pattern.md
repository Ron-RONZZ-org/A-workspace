# Entry Point Registration Pattern

## Rule
Every module that defines a parent Typer app (bundling sub-commands) **must** register it as an entry point under `[project.entry-points."A.commands"]`.

## Bug History
Three modules had parent apps defined in code but never registered as entry points:

| Module | Parent app | Issue | Fix commit |
|--------|-----------|-------|------------|
| A-organizi | `A_organizi.cli:app` | #23 | a5d77dd |
| A-lien | `A_lien.cli:app` | #56 | d1227d8 |
| A-medio | `A_medio.cli:app` | #13 | 5436753 |

## Correct Pattern
Always register BOTH:
1. The parent app (for `A <module>` access):
   ```toml
   module = "A_module.cli:app"
   ```
2. Individual sub-commands (for direct `A <subcommand>` access):
   ```toml
   subcmd = "A_module.cli.sub_cmd:sub_app"
   ```

The lazy plugin loader (`LazyPluginGroup` in A-core) only sees commands listed as entry points. A parent Typer app defined in code but not registered as an entry point is invisible to the CLI.
