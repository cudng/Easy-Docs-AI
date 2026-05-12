import json

import flet as ft

from utils import supabase

SESSION_KEY = "myapp.session"


async def save_session(response):
    payload = {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user_id": response.user.id,
        "email": response.user.email,
        "aud": response.user.aud,
        "expires_at": response.session.expires_at,
    }
    await ft.SharedPreferences().set(SESSION_KEY, json.dumps(payload))


async def load_session() -> dict | None:
    raw = await ft.SharedPreferences().get(SESSION_KEY)
    if not raw:
        return None
    return json.loads(raw)


def get_user(page: ft.Page) -> dict | None:
    """Synchronously read the active user from page.session (set at startup)."""
    return page.session.store.get("user")


async def clear_session(page: ft.Page | None = None):
    """Sign out of Supabase, wipe cached session and in-memory user."""
    try:
        supabase.auth.sign_out()
    except Exception:  # noqa
        pass
    await ft.SharedPreferences().remove(SESSION_KEY)
    if page is not None:
        page.session.store.remove("user")
