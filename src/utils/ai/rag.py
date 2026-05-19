import asyncio

from utils.ai.openrouter import embed_query
from utils.supabase import search_chunks

_GUEST_SYSTEM_PROMPT = (
    "You are a document Q&A assistant. Answer the user's question based "
    "ONLY on the document below. If the answer isn't in the document, say so "
    "plainly. Quote short relevant snippets when helpful."
)

_RAG_SYSTEM_PROMPT = (
    "You are a document Q&A assistant. Answer the user's question using only "
    "the source excerpts below. Cite the source name(s) inline like (foo.pdf) "
    "when you use information from them. If the answer isn't covered, say so."
)

NO_DOCS_REPLY = (
    "There are no documents in this chat to search. "
    "Please upload a document first."
)


def _map_history(history: list[dict]) -> list[dict]:
    return [
        {
            "role": "assistant" if msg["sender"] == "ai" else "user",
            "content": msg["content"],
        }
        for msg in history
    ]


def build_guest_messages(doc_text: str, history: list[dict]) -> list[dict]:
    system_content = f"{_GUEST_SYSTEM_PROMPT}\n\n<document>\n{doc_text}\n</document>"
    return [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_content,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        *_map_history(history),
    ]


async def build_rag_messages(
    chat_id: str, history: list[dict]
) -> tuple[list[dict] | None, list[str]]:
    if not history or history[-1]["sender"] != "user":
        raise ValueError("history must end with a user message")

    user_msg = history[-1]["content"]
    query_embedding = await embed_query(user_msg)
    chunks = await asyncio.to_thread(search_chunks, chat_id, query_embedding, match_count=4)

    if not chunks:
        return None, []

    context_blocks: list[str] = []
    sources: list[str] = []
    seen: set[str] = set()
    for i, chunk in enumerate(chunks, start=1):
        file_name = chunk["file_name"]
        context_blocks.append(f"[Source {i} — {file_name}]\n{chunk['content']}")
        if file_name not in seen:
            seen.add(file_name)
            sources.append(file_name)

    system_content = f"{_RAG_SYSTEM_PROMPT}\n\n" + "\n\n".join(context_blocks)
    messages = [
        {"role": "system", "content": system_content},
        *_map_history(history),
    ]
    return messages, sources
