# A-encik Rewrite Progress

## Completed Issues

| Issue | Title | Commit | Status |
|-------|-------|--------|--------|
| A-core #29 | CRUDService lifecycle hooks | f2758c8 | Closed |
| #8 | Soft Delete / Recycle Bin | 9fc35e3 | Closed |
| #7 | Markdown to HTML Display | a8ebd4e | Closed |
| #4 | ENC Format Import/Export | 37b1aff | Closed |
| #5 | Knowledge Graph Features | 32cdec3 | Closed |
| #6 | Bidirectional Link Reconciliation | 960b8d1 | Closed |
| #9 | AI Generation (generi) | - | Deferred/Closed |

## New Files Created
- `A-encik/src/A_encik/display.py` - HTML rendering using A-core utilities
- `A-encik/src/A_encik/enc_format.py` - ENC parser/serializer (tomllib)

## New CLI Commands
- `encik rubujo list|restaur|malplenigi|forigi` - Recycle bin management
- `encik vidi --html|--open` - HTML display
- `encik eksporti --format enc|json` - Export (default: enc)
- `encik importi <file.enc>` - Import
- `encik serci -s|-S|-L` - Graph-based search
- `encik grafo <ref>` - Visualize relationships
- `encik repacigi` - Reconcile bidirectional links

## Architecture Notes
- Uses A-core `A.core.markdown_parser` and `A.core.markdown_html_view` for HTML display
- Uses A-core CRUDService lifecycle hooks for automatic link reconciliation
- BFS traversal for efficient graph operations
- ENC format uses stdlib `tomllib` (Python 3.11+)

## Deferred
- Issue #9 (AI Generation) - no functional reference in autish-legacy