import flet as ft

from components.utils import AccountMenu
from utils import Config, Style, clear_session


class Appbar(ft.AppBar):
    def __init__(
        self,
        page,
        margin_left: int,
        filename=None,
        on_toggle_sources=None,
        chat_mode=False,
        user_email: str | None = None,
    ):
        self.ref_page = page
        self.sources_shown = False
        self.user_email = user_email
        self.filename = filename
        self.on_toggle_sources = on_toggle_sources
        self.sources_button = (
            ft.Button(
                **Style.resources_visibility_toggle(),
                on_click=self._toggle_sources,
            )
            if chat_mode
            else None
        )

        self.account_control = (
            AccountMenu(page, user_email, on_sign_out=self._on_sign_out)
            if user_email
            else ft.Button(**Style.login_button(), on_click=self.login)
        )

        super().__init__(
            leading_width=275,
            leading=ft.Row(
                [
                    ft.Container(
                        content=ft.Image(Config.SVG, color="#13DAEC"),  # noqa
                        padding=ft.Padding.only(top=10, bottom=10),
                        margin=ft.Margin.only(left=margin_left),
                        on_click=self.go_home,
                    ),
                    ft.Container(
                        ft.Text(**Style.app_name()),
                        on_click=self.go_home,
                    ),
                ],
            ),
            toolbar_height=60,
            title=ft.Text(filename),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LIGHT_MODE
                    if page.theme_mode == ft.ThemeMode.DARK
                    else ft.Icons.DARK_MODE,
                    tooltip="Theme",
                    margin=ft.Margin.only(right=20),
                    on_click=lambda e: self._switch_theme(e),
                ),
                *([self.sources_button] if chat_mode else []),
                self.account_control,
            ],
        )

    def _on_sign_out(self, e=None):
        self.ref_page.run_task(self._sign_out)

    async def _sign_out(self):
        await clear_session(self.ref_page)
        if self.ref_page.route == "/":
            handler = self.ref_page.on_route_change
            if handler:
                handler()
        else:
            await self.ref_page.push_route("/")

    def update_margin(self, w: int):
        self.leading.controls[0].margin.left = w  # noqa

    # ── Theme toggle ────────────────────────────────────────────────
    def _switch_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        e.control.icon = (
            ft.Icons.LIGHT_MODE
            if self.page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.DARK_MODE
        )

    def _toggle_sources(self):
        self.sources_shown = not self.sources_shown
        if self.sources_shown:
            self.sources_button.content = "Hide Sources"
            self.sources_button.icon = ft.Icons.VISIBILITY_OFF
        else:
            self.sources_button.content = "Show Sources"
            self.sources_button.icon = ft.Icons.VISIBILITY
        self.sources_button.update()
        if self.on_toggle_sources:
            self.on_toggle_sources(self.sources_shown)

    async def go_home(self):
        await self.ref_page.push_route("/")

    async def login(self):
        await self.ref_page.push_route("/login")
