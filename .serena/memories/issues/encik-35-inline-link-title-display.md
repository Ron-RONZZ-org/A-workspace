# Bug: serci shows raw markdown/UUID instead of resolved terminologio title

## Issue #35

**Symptoms:**
- Candidate table shows `leĝo de reflekto por [lumo](#63497d2c)` instead of `leĝo de reflekto por lumo`
- Panel shows `rdfs:subClassOf #6356343` instead of `rdfs:subClassOf <Titolo>` (with # prefix on UUID)

**Three root causes fixed in 824918e:**

1. **`entry_locale_title()`** — returned raw terminologio values with `[label](#uuid)` markdown syntax. Added `_strip_inline_links()` helper that strips `[label](#uuid)` → `label`.

2. **`display_ligilo_items()`** — didn't strip `#` prefix from `superklaso` references. Added `.lstrip("#")` before using as UUID in DB lookups.

3. **`_normalise_superklaso_refs()` / `_looks_like_uuid()`** — parser imported UUIDs with `#` prefix (autish-legacy convention) without normalising. Both now strip `#` prefix.

**Systematic review:** Found no other places where raw terminologio values are shown without resolving inline links.
