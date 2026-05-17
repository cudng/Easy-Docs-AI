import os

# load_dotenv() for local dev only, remove/ignore in production
from dotenv import load_dotenv
from postgrest.types import CountMethod
from storage3.types import FileOptions

from supabase import Client, create_client

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")  # noqa
key: str | None = os.environ.get("SUPABASE_KEY")  # noqa

if url and key:
    supabase: Client = create_client(url, key)


DOCUMENTS_BUCKET = "documents"

_CONTENT_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
}


def get_document_by_hash(user_id: str, file_hash: str) -> dict | None:
    res = (
        supabase.table("documents")
        .select("*")
        .eq("user_id", user_id)
        .eq("file_hash", file_hash)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def upload_document_to_storage(
    user_id: str, file_hash: str, ext: str, content: bytes
) -> str:
    storage_path = f"{user_id}/{file_hash}.{ext}"
    file_options: FileOptions = {
        "content-type": _CONTENT_TYPES.get(ext, "application/octet-stream"),
    }
    supabase.storage.from_(DOCUMENTS_BUCKET).upload(
        path=storage_path,
        file=content,
        file_options=file_options,
    )
    return storage_path


def insert_document(
    user_id: str,
    file_name: str,
    storage_path: str,
    size_bytes: int,
    file_hash: str,
) -> dict:
    res = (
        supabase.table("documents")
        .insert(
            {
                "user_id": user_id,
                "file_name": file_name,
                "storage_path": storage_path,
                "size_bytes": size_bytes,
                "file_hash": file_hash,
                "status": "ready",
            }
        )
        .execute()
    )
    return res.data[0]


def update_document_status(document_id: str, status: str) -> None:
    supabase.table("documents").update({"status": status}).eq(
        "id", document_id
    ).execute()


def delete_storage_object(storage_path: str) -> None:
    supabase.storage.from_(DOCUMENTS_BUCKET).remove([storage_path])


def create_chat(user_id: str, title: str) -> dict:
    res = supabase.table("chats").insert({"user_id": user_id, "title": title}).execute()
    return res.data[0]


def delete_chat(chat_id: str) -> None:
    linked = (
        supabase.table("chat_documents")
        .select("document_id")
        .eq("chat_id", chat_id)
        .execute()
    )
    doc_ids = [row["document_id"] for row in linked.data]

    supabase.table("chat_documents").delete().eq("chat_id", chat_id).execute()
    supabase.table("chats").delete().eq("id", chat_id).execute()

    for doc_id in doc_ids:
        remaining = (
            supabase.table("chat_documents")
            .select("document_id", count=CountMethod.exact)
            .eq("document_id", doc_id)
            .execute()
        )
        if (remaining.count or 0) > 0:
            continue

        doc_res = (
            supabase.table("documents")
            .select("storage_path")
            .eq("id", doc_id)
            .limit(1)
            .execute()
        )
        if not doc_res.data:
            continue

        storage_path = doc_res.data[0]["storage_path"]
        try:
            delete_storage_object(storage_path)
        except Exception as err:
            print(f"Failed to delete storage object {storage_path}: {err}")
        supabase.table("documents").delete().eq("id", doc_id).execute()


def list_chats(user_id: str) -> list[dict]:
    res = (
        supabase.table("chats")
        .select("id, title, updated_at")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return res.data


def count_user_chats(user_id: str) -> int:
    res = (
        supabase.table("chats")
        .select("id", count=CountMethod.exact)
        .eq("user_id", user_id)
        .execute()
    )
    return res.count or 0


def link_chat_document(chat_id: str, document_id: str) -> None:
    supabase.table("chat_documents").insert(
        {"chat_id": chat_id, "document_id": document_id}
    ).execute()


def count_chat_documents(chat_id: str) -> int:
    res = (
        supabase.table("chat_documents")
        .select("document_id", count=CountMethod.exact)
        .eq("chat_id", chat_id)
        .execute()
    )
    return res.count or 0


def get_chat_documents(chat_id: str) -> list[dict]:
    res = (
        supabase.table("chat_documents")
        .select("documents(*)")
        .eq("chat_id", chat_id)
        .execute()
    )
    return [row["documents"] for row in res.data if row.get("documents")]


def get_messages(chat_id: str) -> list[dict]:
    res = (
        supabase.table("messages")
        .select("*")
        .eq("chat_id", chat_id)
        .order("created_at")
        .execute()
    )
    return res.data


def insert_message(chat_id: str, sender: str, content: str) -> dict:
    res = (
        supabase.table("messages")
        .insert({"chat_id": chat_id, "sender": sender, "content": content})
        .execute()
    )
    return res.data[0]


def update_chat_title(chat_id: str, title: str) -> None:
    supabase.table("chats").update({"title": title}).eq("id", chat_id).execute()


def count_document_chunks(document_id: str) -> int:
    res = (
        supabase.table("document_chunks")
        .select("id", count=CountMethod.exact)
        .eq("document_id", document_id)
        .execute()
    )
    return res.count or 0


def insert_chunks(
    document_id: str, chunks: list[str], embeddings: list[list[float]]
) -> None:
    assert len(chunks) == len(embeddings), "chunks and embeddings length mismatch"
    if not chunks:
        return
    rows = [
        {
            "document_id": document_id,
            "chunk_index": i,
            "content": content,
            "embedding": embedding,
        }
        for i, (content, embedding) in enumerate(zip(chunks, embeddings))
    ]
    supabase.table("document_chunks").insert(rows).execute()


def search_chunks(
    chat_id: str, query_embedding: list[float], match_count: int = 4
) -> list[dict]:
    res = supabase.rpc(
        "match_document_chunks",
        {
            "query_embedding": query_embedding,
            "chat_id_filter": chat_id,
            "match_count": match_count,
        },
    ).execute()
    return res.data or []
