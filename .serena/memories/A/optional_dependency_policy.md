# Optional Dependency Handling Policy

## Rule
Whenever a command requires an optional dependency that is not installed, do NOT just show an error message. **Offer to install it for the user.**

## Pattern
```python
try:
    import keyring
except ImportError:
    answer = typer.confirm(
        tr_multi(
            "Necesas 'keyring' biblioteko. Ĉu instali ĝin nun?",
            "The 'keyring' library is required. Install it now?",
            "La bibliothèque 'keyring' est nécessaire. Installer maintenant ?",
        ),
        default=True,
    )
    if answer:
        import subprocess, sys
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "keyring"]
        )
        import keyring
    else:
        raise typer.Exit(1)
```

## When to apply
- All CLI commands that need optional deps (keyring, yt-dlp, siege, etc.)
- Migration scripts
- Any runtime feature detection

## Where applied
- `A migri-keyring`: keyring lib ✓ (first instance)
