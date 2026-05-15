import flet as ft

from utils import Config, Style, clear_session


class Appbar(ft.AppBar):
    def __init__(
        self,
        page,
        margin_left: int,
        user_email: str | None = None,
        documents: list[str] | None = None,
        on_menu_click=None,
        show_menu_icon: bool = False,
    ):
        self.ref_page = page
        self.user_email = user_email
        self.documents = documents or []
        self.on_menu_click = on_menu_click

        self.menu_icon = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Toggle chats",
            icon_color=Config.PRIMARY,
            on_click=self._on_menu_click,
            visible=show_menu_icon,
        )

        actions: list[ft.Control] = []
        if self.documents:
            actions.append(
                ft.Container(
                    margin=ft.Margin.only(right=4),
                    content=ft.PopupMenuButton(
                        content=ft.Container(
                            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            border_radius=8,
                            content=ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.FOLDER_OPEN,
                                        size=18,
                                        color=Config.PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Documents ({len(self.documents)})",
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                        font_family=Config.FONT,
                                    ),
                                ],
                                spacing=8,
                                tight=True,
                            ),
                        ),
                        tooltip="Selected documents",
                        items=self._build_document_items(),
                    ),
                ),
            )
        actions.append(
            ft.Container(
                margin=ft.Margin.only(right=20),
                content=ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    tooltip="Menu",
                    items=self._build_menu_items(),
                    icon_color=Config.PRIMARY,
                ),
            ),
        )

        super().__init__(
            leading_width=275,
            leading=ft.Row(
                [
                    self.menu_icon,
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
            title=None,
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            actions=actions,
        )

    # ── Document items ──────────────────────────────────────────────
    DOC_ITEM_WIDTH = 280

    def _build_document_items(self):
        items: list[ft.PopupMenuItem] = []
        for name in self.documents:
            items.append(
                ft.PopupMenuItem(
                    content=ft.Container(
                        width=self.DOC_ITEM_WIDTH,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.INSERT_DRIVE_FILE_OUTLINED,
                                    size=18,
                                    color=ft.Colors.OUTLINE,
                                ),
                                ft.Text(
                                    name,
                                    size=13,
                                    font_family=Config.FONT,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                    tooltip=name,
                                ),
                            ],
                            spacing=10,
                            tight=True,
                        ),
                    ),
                    on_click=lambda _e: None,
                )
            )
        return items

    # ── Menu items ──────────────────────────────────────────────────
    def _build_menu_items(self):
        items: list[ft.PopupMenuItem] = []

        if self.user_email:
            items.append(
                ft.PopupMenuItem(
                    content=ft.Container(
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Signed in as",
                                    size=11,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                                ft.Text(
                                    self.user_email,
                                    size=13,
                                    color=Config.TEAL,
                                    weight=ft.FontWeight.W_600,
                                    font_family=Config.FONT,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                            spacing=2,
                            tight=True,
                        ),
                    ),
                    on_click=lambda _e: None,
                )
            )
            items.append(ft.PopupMenuItem())  # divider

        is_dark = self.ref_page.theme_mode == ft.ThemeMode.DARK
        items.append(
            ft.PopupMenuItem(
                "Light theme" if is_dark else "Dark theme",
                icon=ft.Icons.LIGHT_MODE if is_dark else ft.Icons.DARK_MODE,
                on_click=self._switch_theme,
            )
        )

        items.append(ft.PopupMenuItem())  # divider

        if self.user_email:
            items.append(
                ft.PopupMenuItem(
                    "Sign out",
                    icon=ft.Icons.LOGOUT,
                    on_click=self._on_sign_out,
                )
            )
        else:
            items.append(
                ft.PopupMenuItem(
                    "Sign in",
                    icon=ft.Icons.LOGIN,
                    on_click=self._on_sign_in,
                )
            )

        return items

    # ── Sign in / out ───────────────────────────────────────────────
    def _on_sign_in(self, e=None):
        self.ref_page.run_task(self._sign_in)

    async def _sign_in(self):
        await self.ref_page.push_route("/login")

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

    # ── Menu toggle ─────────────────────────────────────────────────
    def _on_menu_click(self, e=None):
        if self.on_menu_click is not None:
            self.on_menu_click(e)

    def set_menu_visible(self, visible: bool):
        self.menu_icon.visible = visible

    # ── Misc ────────────────────────────────────────────────────────
    def update_margin(self, w: int):
        # leading row is [menu_icon, logo_container, name_container]
        self.leading.controls[1].margin.left = w  # noqa

    def _switch_theme(self, e=None):
        self.ref_page.theme_mode = (
            ft.ThemeMode.DARK
            if self.ref_page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        # Rebuild items so the theme label/icon flips on next open
        self.actions[0].content.items = self._build_menu_items()
        self.ref_page.update()

    async def go_home(self):
        await self.ref_page.push_route("/")
