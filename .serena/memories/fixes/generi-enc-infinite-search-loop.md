# Fix: Infinite search loop in `generi --formato enc`

## Symptom
`A agento generi -f enc "Grokipedia"` failed with:
```
Generado malsukcesis: LLM returned raw tool output instead of generated content
```

## Root Causes

### A. Prompt encouraged endless searching
File: `src/A_agento/prompts/generi_enc.md`
The instruction said "if not found, try alternative search terms / if always not found, leave blank, do NOT assume" with NO stop condition. The LLM would keep trying alternative searches for entities not in the database (Elon Musk, Grok, xAI, etc.).

### B. max_turns exhaustion returned garbage
File: `src/A_agento/tools/executor.py`
After max_turns=30, if the last response had `tool_calls`, `response.content` was empty/None. The code returned it directly, and `_clean_enc_output` rejected it as raw tool output.

### C. Raw output retry was one-shot
Same file. The retry used the same message every time with no escalation — the LLM could ignore it and return raw output again, and the content would propagate.

## Fix (commit 0772edd)

### executor.py
- **After max_turns:** Force one final `provider.chat(messages, tools=None)` WITHOUT tool access + safety-net second attempt if content is still empty/raw
- **Raw output retry:** Add `raw_output_retries` counter with 3 escalating messages (hint → strong hint → "STOP" command)

### generi_enc.md
- Added explicit "at most 2 attempts" limit per entity
- Added "CRITICAL: Search limit" section at end: max 3 searches per entity, 5 total before generating with existing knowledge

### test_tools.py
- 4 new tests: max_turns with tool_calls, raw output escalation, combined scenario, empty content at max_turns
