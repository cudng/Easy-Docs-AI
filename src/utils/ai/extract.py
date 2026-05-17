import io
import re

import docx
import pypdf

_BLANK_LINES_RE = re.compile(r"\n{3,}")


def extract_text(file_name: str, content: bytes) -> str:
    ext = file_name.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        text = _extract_pdf(content)
    elif ext == "docx":
        text = _extract_docx(content)
    elif ext == "txt":
        text = content.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    return _BLANK_LINES_RE.sub("\n\n", text).strip()


def _extract_pdf(content: bytes) -> str:
    reader = pypdf.PdfReader(io.BytesIO(content))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            pages.append(text.strip())
    return "\n\n".join(pages)


def _extract_docx(content: bytes) -> str:
    document = docx.Document(io.BytesIO(content))
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)
