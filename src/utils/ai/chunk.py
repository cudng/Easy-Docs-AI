def chunk_text(
    text: str, *, max_chars: int = 1500, overlap: int = 200
) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    text_len = len(text)
    half = max_chars // 2

    while start < text_len:
        end = min(start + max_chars, text_len)

        if end < text_len:
            window = text[start:end]
            for sep in ("\n\n", "\n", ". "):
                idx = window.rfind(sep)
                if idx > half:
                    end = start + idx + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_len:
            break
        start = max(end - overlap, start + 1)

    return chunks
