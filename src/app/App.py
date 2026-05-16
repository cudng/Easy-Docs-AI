import flet as ft

from routes import RouteHandler
from utils import Config, clear_session, load_session, save_session, supabase


async def main(page: ft.Page):
    page.fonts = Config.PAGE_FONTS
    page.theme = Config.THEME
    page.dark_theme = Config.DARK_THEME

    session: dict | None = await load_session()

    if session:
        try:
            response = supabase.auth.set_session(
                session["access_token"], session["refresh_token"]
            )
            if response.session:
                await save_session(response)
                page.session.store.set(
                    "user",
                    {"user_id": response.user.id, "email": response.user.email},
                )
        except Exception:  # noqa
            await clear_session(page)

    router = RouteHandler(page)

    page.on_route_change = router.route
    page.on_view_pop = router.view_pop

    page.file_picker = ft.FilePicker()

    # Flet 0.81+: call the route handler directly for the initial render.
    # push_route() is async and only used for in-app navigation clicks.
    router.route()

    # await page.push_route("/register")
