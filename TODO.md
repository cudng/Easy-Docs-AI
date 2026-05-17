# RAG / LLM integration — progress

Source plan: `~/.claude/plans/chat-is-mostly-working-curried-pebble.md`

## Architecture (two paths)

- **Guest** (1 doc, ≤ 5 MB) — text extracted at upload, stored in browser via `SharedPreferences` (`doc_text_{chat_id}`), sent verbatim as system context every turn. No embeddings, no DB.
- **Logged-in** (up to 3 docs) — text extracted → chunked → embedded → stored in Supabase `document_chunks` (pgvector 2048-dim). On every user message, query is embedded and top-K chunks are retrieved via the `match_document_chunks` RPC and sent as context.

Both paths share the same OpenRouter chat completion client.

## Done

### Step 1 — Dependencies + env
- [x] Added `openai`, `pypdf`, `python-docx` to `pyproject.toml`.
- [x] Added `.env` keys: `OPENROUTER_API_KEY`, `OPENROUTER_CHAT_MODEL`, `OPENROUTER_EMBED_MODEL`, `OPENROUTER_SITE_URL`, `OPENROUTER_APP_NAME`.

### Step 2 — OpenRouter client (`src/utils/ai/openrouter.py`)
- [x] `AsyncOpenAI` client pointed at `https://openrouter.ai/api/v1`.
- [x] Default headers: `HTTP-Referer`, `X-Title`.
- [x] `chat_completion(messages, *, max_tokens=1024)` — async.
- [x] `embed_texts(texts)` — async, uses multimodal input format required by `nvidia/llama-nemotron-embed-vl-1b-v2:free`.
- [x] `embed_query(text)` — async wrapper.
- [x] Verified embedding dim = 2048.

### Step 3 — Supabase pgvector schema
- [x] `vector` extension enabled.
- [x] `document_chunks` table: `id`, `document_id` FK (ON DELETE CASCADE), `chunk_index`, `content`, `embedding vector(2048)`, `created_at`.
- [x] B-tree index on `document_id`.
- [x] No vector index (pgvector caps HNSW/ivfflat at 2000 dims; falls back to sequential scan, fine at current scale).
- [x] RPC `match_document_chunks(query_embedding, chat_id_filter, match_count)` — joins through `chat_documents`, returns top-K by cosine.
- [x] RLS enabled on `document_chunks`; SELECT / INSERT / DELETE policies scoped to "user owns the parent document".

### Step 4 — Extraction + chunking
- [x] `src/utils/ai/extract.py` — `extract_text(file_name, content)` dispatches on `.pdf` / `.docx` / `.txt`. Whitespace cleanup.
- [x] `src/utils/ai/chunk.py` — `chunk_text(text, *, max_chars=1500, overlap=200)`. Sliding window prefers `\n\n` → `\n` → `. ` boundaries.

### Step 5 — Supabase chunk helpers (`src/utils/supabase.py`)
- [x] `insert_chunks(document_id, chunks, embeddings)` — batched insert.
- [x] `search_chunks(chat_id, query_embedding, match_count=4)` — calls the RPC.
- [x] `count_document_chunks(document_id)` — added for the dedup backfill path.
- [x] Re-exported from `src/utils/__init__.py`.

### Step 6 — Message builders (`src/utils/ai/rag.py`)
- [x] `build_guest_messages(doc_text, history)` — system prompt + full doc + history (last entry is the new user message).
- [x] `build_rag_messages(chat_id, history) -> (messages | None, sources)` — embeds query, retrieves top-K via RPC, formats source blocks; returns `(None, [])` if no chunks so caller can short-circuit with `NO_DOCS_REPLY` instead of wasting an LLM call.
- [x] `NO_DOCS_REPLY` constant.

### Step 7 — Upload pipeline (`src/components/upload_card.py`)
- [x] "Processing…" button state during the async pipeline.
- [x] Guest branch: extract text → write `uploaded_files_{chat_id}` and `doc_text_{chat_id}` to `SharedPreferences` (JSON-encoded for lists, raw string for text).
- [x] Logged-in branch: extract → chunk → embed → upload to storage → `insert_document` → `insert_chunks`. Cleanup on failure deletes orphan storage objects.
- [x] Dedup backfill: when an existing document is reused via hash, check `count_document_chunks` and embed if missing (handles docs uploaded before the chunks pipeline existed).

### Step 8 — LLM wired into chat (`src/views/chat.py`)
- [x] Imports `chat_completion`, `build_rag_messages`, `build_guest_messages`, `NO_DOCS_REPLY`.
- [x] `_process` in `_handle_send` replaces the simulated response. Branches on `is_logged_in`. Calls awaited directly (no `to_thread`) since the OpenAI client is async.
- [x] Exceptions surface as a friendly bubble; user message still persists.

### Step 9 — Source attribution UI (`src/components/chat/messages.py`)
- [x] `AiMessage(text, sources=None)` — optional sources list.
- [x] When sources non-empty, renders a simple bordered Column listing them.
- [x] When sources empty, source block is omitted from the widget tree (no hidden ExpansionTile).
- [x] Removed the previous hardcoded "PAGE 4, PARAGRAPH 2" / "Enterprise cloud segment…" mock data.
- [x] `_add_ai_message(text, sources=None)` passes sources through. Loading-remove and bubble-append batched into a single `update()`.

### Cross-cutting / refactors
- [x] `chat.py._load_chat_data` async (`SharedPreferences` is async).
- [x] `chat.py.__init__` defers load to `page.run_task(self._setup_async)` instead of blocking init.
- [x] `chat.py.load_chat` (route handler) async; `route.py` calls it via `page.run_task`.
- [x] `_add_user_message` / `_add_ai_message` async; guest history writes go to `SharedPreferences`.
- [x] JSON encoding for `SharedPreferences` complex values (works around Flutter's `List<String>` cast strictness).
- [x] `delete_chat` cascades: collects linked `document_id`s, deletes join rows + chat, then for any document with zero remaining `chat_documents` references deletes the storage object and the `documents` row (chunks cascade automatically).

## Still to do

### Step 10 — Full end-to-end test
- [ ] **Blocked by the UI freeze bug** (see Known issues). End-to-end can't be ticked off until the page stops becoming unresponsive on AI reply.
- [ ] Guest: upload PDF → ask a doc-grounded question → expect a real grounded reply.
- [ ] Guest: ask a question the doc doesn't answer → expect "not in document" style reply.
- [ ] Logged-in: upload 2 PDFs → ask question hitting doc A → reply shows sources containing A.
- [ ] Logged-in: ask question hitting doc B → sources flip to B.
- [ ] Logged-in: reload page → history persists, sources still rendered for prior replies.
- [ ] Verify `select count(*) from document_chunks where document_id = '<id>'` matches expected chunk count.
- [ ] Failure modes: bad / encrypted PDF surfaces a snackbar; broken API key surfaces "Sorry — couldn't reach the model" bubble; user message still persists.

### Nice-to-have (not in original plan)
- [ ] Allow attaching a doc to an existing chat (currently each chat is born with its docs at creation time).
- [ ] Source citations clickable / show chunk content on click.
- [ ] Streaming responses (would require `AiMessage` to accept incremental text updates).
- [ ] Per-user storage quota check before upload (sum `size_bytes`).
- [ ] Token-budget guard for the guest path (truncate `doc_text` if it would overflow the model's context).
- [ ] Document deletion UI surfacing the existing server-side cascade.

## Known issues (deferred)

- **Page Unresponsive in Chrome after AI reply renders.** Python completes the full pipeline cleanly (verified via prints), DB write succeeds, navigating away and back shows the message correctly — so the freeze is purely client-side Flutter rendering. Suspects investigated and addressed: hardcoded `ExpansionTile` mock data removed; `BoxShadow` on bubbles removed per [Flutter #95949](https://github.com/flutter/flutter/issues/95949); long unconstrained Russian text capped at `width=700`. Still triggers under some condition; needs further isolation.
- **Llama 3.3 70B free model rate-limits hard (429).** Workaround: change `OPENROUTER_CHAT_MODEL` in `.env` to `google/gemini-2.0-flash-exp:free` or `deepseek/deepseek-chat-v3.1:free`.

## Out of scope (separate work)

- Authentication hardening / RLS audit of all tables (only `document_chunks` policies were added in this work).
- Production deployment (env vars, OpenRouter prod key, storage quota, monitoring).
