import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

_API_KEY = os.environ["OPENROUTER_API_KEY"]
_CHAT_MODEL = os.environ["OPENROUTER_CHAT_MODEL"]
_EMBED_MODEL = os.environ["OPENROUTER_EMBED_MODEL"]
_SITE_URL = os.environ.get("OPENROUTER_SITE_URL", "")
_APP_NAME = os.environ.get("OPENROUTER_APP_NAME", "EasyDocs-AI")

_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=_API_KEY,
    default_headers={
        "HTTP-Referer": _SITE_URL,
        "X-Title": _APP_NAME,
    },
)


async def chat_completion(messages: list[dict], *, max_tokens: int = 1024) -> str:
    response = await _client.chat.completions.create(
        model=_CHAT_MODEL,
        messages=messages,  # type: ignore[arg-type]
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


async def chat_completion_stream(messages: list[dict], *, max_tokens: int = 1024):
    stream = await _client.chat.completions.create(
        model=_CHAT_MODEL,
        messages=messages,  # type: ignore[arg-type]
        max_tokens=max_tokens,
        stream=True,
    )
    async for event in stream:
        if not event.choices:
            continue
        delta = event.choices[0].delta
        if delta and delta.content:
            yield delta.content


async def embed_texts(texts: list[str]) -> list[list[float]]:
    response = await _client.embeddings.create(
        model=_EMBED_MODEL,
        input=[{"content": [{"type": "text", "text": t}]} for t in texts],  # type: ignore[arg-type]
        encoding_format="float",
    )
    return [item.embedding for item in response.data]


async def embed_query(text: str) -> list[float]:
    return (await embed_texts([text]))[0]
