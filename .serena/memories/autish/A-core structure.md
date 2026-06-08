# A-core Project Structure

## Location
`/home/rongzhou/kodo/autish/`

## Directory Structure
```
/home/rongzhou/kodo/autish/
├── A-core/           # Core CLI framework (own git repo)
├── A-tempo/         # Time/clock plugin
├── A-sistemo/       # System management plugin
├── A-vorto/         # Wordbook plugin
├── A-encik/        # Knowledge plugin
├── A-organizi/      # Calendar/todo/journal plugin
├── A-lien/        # Email/contacts plugin
├── A-medio/        # Video/photo/audio plugin
└── autish-legacy/  # Old autish v0.0.2 code (read-only reference)
```

## Key Points
- Each A-* folder is its own git repo with GitHub remote
- A-core imports: `from A.core import ...` (not relative paths)
- Working branch for issues #2,#3: `feat/uzanto-config`
- PR: https://github.com/Ron-RONZZ-org/A-core/pull/4
- Issues #2,#3 have consultant approval comments attached

## Always Use Absolute Paths
When working in `/home/rongzhou/kodo/autish/`, use full paths:
- `/home/rongzhou/kodo/autish/A-core/src/A/core/config.py`
- `/home/rongzhou/kodo/autish/A-tempo/src/`