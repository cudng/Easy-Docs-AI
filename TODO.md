# Persistence & limits — progress

Source plan: `~/.claude/plans/velvet-wandering-sloth.md`

## Done

### Step 1 — Schema + RLS + storage
- [x] `documents`, `chats`, `chat_documents`, `messages` tables with RLS policies and indexes.
- [x] `set_updated_at()` trigger function + `chats_set_updated_at` trigger.
- [x] `pgvector` extension enabled (via Supabase dashboard).
- [x] Private `documents` bucket with per-user-prefix storage policies (SELECT / INSERT / DELETE).
- [x] Versioned migration at `supabase/migrations/20260514000000_initial_schema.sql`.

### Step 2 — Upload flow rewrite (`src/views/session.py`)
- [x] Supabase helpers added to `src/utils/supabase.py` (`get_document_by_hash`, `upload_document_to_storage`, `insert_document`, `update_document_status`, `delete_storage_object`, `create_chat`, `link_chat_document`).
- [x] `pick_files(with_data=True)` so bytes are available on web.
- [x] Per-file size cap (5 MB, matches DB `CHECK`) enforced **before** upload.
- [x] Branch on `get_user()`: guest stays in-memory; logged-in goes through Supabase.
- [x] Logged-in flow: SHA-256 hash → dedup via `get_document_by_hash` → upload to bucket at `<user_id>/<file_hash>.<ext>` → insert `documents` row → create `chats` row → link via `chat_documents`.
- [x] Failure cleanup: orphan storage objects deleted on insert failure; chat creation aborted on any error.

### Step 3 — Route / id semantics (`src/views/chat.py` + `session.py`)
- [x] `doc_id` → `chat_id` rename in `chat.py`.
- [x] UUID validation on the route segment (`uuid.UUID(raw_chat_id)`); invalid → redirect to `/session`.
- [x] Guest `session.store` key renamed `uploaded_file_<id>` → `uploaded_files_<chat_id>` (matched in both files).
- [x] Guest path now uses hyphenated UUIDs (matches DB format).

### Step 4 — Chat persistence (`src/views/chat.py`)
- [x] DB-backed history load for logged-in users (`get_chat_documents`, `get_messages`).
- [x] DB inserts in `_add_user_message` / `_add_ai_message` for logged-in users.
- [x] Auto-title: first user message updates `chats.title` (cap 75 chars).
- [x] `role` → `sender` rename to match DB enum.
- [x] Threading cleanup: `threading.Thread` + `time.sleep` → `page.run_task` + `asyncio.sleep`.
- [x] No more `session.store` dual write for logged-in users.

## Still to do

### Step 5 — Quota checks
- [x] Before creating a chat: count `chats` rows for the user; reject if `>= 10` with a SnackBar.
- [x] ~~Before linking a doc to a chat: count `chat_documents` rows for that chat; reject if `>= 3` with a SnackBar.~~ Skipped — currently redundant: chat is created fresh in the same flow (count = 0) and `max_files = 3` + slice in `session.py` already cap the upload. Revisit if an "add doc to existing chat" view is added.
- [ ] (Optional) max total storage per user — sum `size_bytes` before upload.

### Step 6 — Remaining cleanup
- [x] Threading → `page.run_task` (done in step 4).
- [x] Remove dual write to `session.store` for logged-in users (done in step 4).
- [ ] `import threading` already removed — verify nothing else in the repo depends on the old `session.store` keys for logged-in users.

## Manual verification checklist

- [ ] Guest: upload 1 file → chat works → refresh → chat is gone (expected).
- [ ] Logged user: upload 1 file → row in `documents`, object in bucket, chat row + junction row → send messages → rows in `messages`.
- [ ] First user message updates `chats.title` from filename to message text.
- [ ] Refresh on logged-in chat page → history reloads from DB.
- [ ] Try uploading a file > 5 MB → rejected pre-upload (no storage object, no DB row).
- [ ] Try creating an 11th chat → rejected with UI message.
- [ ] Try linking a 4th document to a chat → currently capped client-side by `max_files = 3`; no server-side check.
- [ ] Same file uploaded twice → no duplicate storage object; new junction row links to existing document.
- [ ] Log in as user B → cannot see user A's documents/chats/messages (RLS).
- [ ] Tamper URL with random UUID → bounces to `/session`.
- [ ] Fetch another user's storage object via direct URL → denied.

## Out of scope (separate plans)

- RAG pipeline (chunking, embeddings, retrieval).
- Real LLM integration replacing the simulated response in `chat.py`.
- Streaming responses, token accounting, per-user rate limiting.
