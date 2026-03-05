import flet as ft

from routes import RouteHandler
from utils import Config


def main(page: ft.Page):
    page.fonts = Config.PAGE_FONTS
    page.theme = Config.THEME
    page.dark_theme = Config.DARK_THEME

    router = RouteHandler(page)

    page.on_route_change = router.route
    page.on_view_pop = router.view_pop

    # Flet 0.81+: call the route handler directly for the initial render.
    # push_route() is async and only used for in-app navigation clicks.
    router.route()
