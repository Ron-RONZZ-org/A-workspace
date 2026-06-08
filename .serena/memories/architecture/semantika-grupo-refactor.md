# Semantika grupo refactor plan

## Decision
Move dynamic group subcommands (generala, abstrakta, persono, geografio) under a `grupo` sub-typer to avoid namespace pollution.

## Command tree (after refactor)
```
encik semantika                    (no_args_is_help=True)
├── serci <query>                  unchanged
├── aldoni <id> <group>            unchanged
├── forigi <id> <group>            unchanged
├── modifi <id> <group>            unchanged
└── grupo                          NEW sub-typer
    ├── ls                         was: semantika ls
    ├── vidi <name>                was: semantika <group_name>
    ├── aldoni <name>              create new group (new CSV)
    ├── modifi <old> <new>         rename group (rename CSV)
    └── forigi <name>              delete group (remove CSV + --jes confirmation)
```

## Key changes
1. Remove `_register_semantika_group_commands()` and dynamic command registration
2. `semantika_app`: `no_args_is_help=True` instead of callback
3. `config.py`: add `create_semantika_group()`, `rename_semantika_group()`, `delete_semantika_group()`
4. `_RESERVED_SUBCOMMANDS`: add "grupo"
5. `cli.py`: remove registration call at startup

## Issue
https://github.com/Ron-RONZZ-org/A-encik/issues/41
