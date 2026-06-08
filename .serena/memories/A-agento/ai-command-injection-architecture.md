## Cross-Module AI Command Injection (#20)

### Architecture

A-core's `A.core.plugin_loader` now supports a `"A.ai_commands"` entry point group.
When loading a plugin, it checks for matching entry points and injects AI commands
as a named sub-app (`ai`) in the module's Typer app.

### Entry Points in A-agento

```toml
[project.entry-points."A.ai_commands"]
lien = "A_agento.registration:get_lien_ai_app"
encik = "A_agento.registration:get_encik_ai_app"
```

### Module Structure

- `commands/email.py` — resumu, respondi, agu (standalone Typer-compatible functions)
- `commands/knowledge.py` — generi (moved from A-encik, now implemented)
- `commands/_helpers.py` — get_provider_or_exit(), confirm_action()
- `registration.py` — factory functions returning Typer sub-apps
- `cli.py` — thin wrapper (42 lines) importing from commands/ and registration

### Testing

Mock paths changed: patch `A.core.ai.get_provider` and `A_agento.service.get_agent_service`
(since these are imported lazily inside command functions, not at module level).
