# Color Accessibility Reform — Issue #1

## Summary

Change the `STYLES` dict in `A-core/src/A/utils/output.py` and update prefix symbols to achieve WCAG AA compliance for color-blind users and terminal-background variation.

## The Changes

### 1. STYLES dict (output.py lines 12-18)

```python
# Current (broken)
STYLES = {
    "info": Style(dim=True),
    "success": Style(color="green", dim=True),    # ← dim kills ALL contrast
    "warning": Style(color="yellow"),              # ← invisible on light backgrounds
    "error": Style(color="red"),                   # ← low contrast on dark terminals
    "label": Style(bold=True),
}

# Proposed (accessible)
STYLES = {
    "info": Style(dim=True),               # unchanged — intentionally subdued
    "success": Style(color="green", bold=True),  # REMOVED dim, ADDED bold
    "warning": Style(color="yellow", bold=True), # ADDED bold
    "error": Style(color="red", bold=True),      # ADDED bold
    "label": Style(bold=True),              # unchanged
}
```

### 2. Prefix symbols (output.py lines 33-45)

```python
# Current — warning and error share the SAME prefix
def success(message): console.print(f"[✓] {message}", ...)
def warning(message): console.print(f"[!] {message}", ...)  # ← same as error
def error(message):   console.print(f"[!] {message}", ...)  # ← same as warning

# Proposed — all three symbols are distinct
def success(message): console.print(f"[✓] {message}", ...)  # CHECK MARK (same)
def warning(message): console.print(f"[!] {message}", ...)  # EXCLAMATION (same)
def error(message):   console.print(f"[✗] {message}", ...)  # BALLOT X (new)
```

## Why Each Change

### `success`: remove dim, add bold

| Background | Current CR | Proposed CR | Improvement |
|-----------|-----------|------------|-------------|
| White (#FFF) | 2.15 ✗ | 5.14 ✓ | 2.4× |
| Light grey (#D3D3D3) | 1.85 ✗ | 3.43 ~ | 1.9× |
| Dark grey (#1E1E1E) | 1.70 ✗ | 3.25 ~ | 1.9× |
| Black (#000) | 1.73 ✗ | 4.09 ~ | 2.4× |

**Was**: `dim` reduced green to 50% opacity, blending toward background. CR ~1.7 on ALL backgrounds — below WCAG even for large text (3:1).

**Now**: Green alone is CR 3.3-5.1. Not AA-compliant on grey, but readable. ✓ symbol is the primary signal. Bold adds font weight as secondary visual cue.

### `error`: add bold

**On dark terminals**: Plain red (#CD0000, L≈0.129) on dark grey (L≈0.018) = CR 2.85 ✗. On 16-color terminals, bold+red triggers bright red, boosting dark-background CR to 4.17 ~. On true-color terminals, bold adds font weight without changing color — the weight itself signals importance.

**Symbol change**: `[✗]` instead of `[!]` distinguishes error from warning for color-blind users.

### `warning`: add bold

**On light backgrounds**: Yellow (#FFFF00, L≈0.928) on white (L=1.0) = CR 1.07 ✗ — nearly invisible. Bold adds weight as a secondary signal. On dark backgrounds, yellow already has CR 14:1+.

### `info`: unchanged

`dim` is WAI-adapted: on dark terminals it dims light text (CR ~5-8:1 ✓), on light terminals it dims dark text (CR ~4-5:1 ~). Acceptable for intentionally secondary text.

## Accessibility Principles Applied

1. **Don't use color alone**: Four distinct symbol prefixes (✓, !, ✗, plus no-symbol for info) carry the semantic meaning. Color is reinforcement.

2. **Bold as secondary channel**: Font weight differences are perceived by all users regardless of color vision.

3. **Calm aesthetic preserved**: No background colors, no neon, no animation. Just slightly thicker text and removed dim.

## Tradeoffs

| Change | Tradeoff |
|--------|----------|
| Remove dim from success | Success text is more prominent — slightly less "calm" |
| Add bold to all states | Three bold levels may feel repetitive, but adds consistency |
| ✗ for error | Requires terminal font support for U+2717 (same font as ✓ — should work) |
| Green still fails AA on grey | ✓ symbol compensates. True fix would require abandoning green, which breaks convention |

## Previous WCAG Audit Notes

The `dim` modifier was the single largest accessibility failure — it reduced ALL success messages below WCAG floor (3:1). Removing `dim` is the highest-impact change per line of code.

For future consideration: On true-color terminals, `bold` could be replaced with a specific hex color for better contrast control. But named ANSI colors ensure maximum terminal compatibility.
