import flet as ft

from utils import Config, Style, clear_session
from utils.utils import Breakpoint


class Appbar(ft.AppBar):
    def __init__(
        self,
        page,
        user_email: str | None = None,
        documents: list[str] | None = None,
        on_menu_click=None,
        show: bool = False,
    ):
        self.ref_page = page
        self.user_email = user_email
        self.documents = documents or []
        self.on_menu_click = on_menu_click
        is_narrow = (page.width or 1200) < Breakpoint.MOBILE_BREAKPOINT

        self.menu_icon = ft.IconButton(
            **Style.menu_icon(show),
            on_click=self._on_menu_click,
        )

        self.documents_container = ft.Container(
            **Style.documents_menu(
                self._build_document_items(), len(self.documents)
            ),
            visible=bool(self.documents),
        )
        menu_button_kwargs = Style.menu_button(self._build_menu_items())
        self.menu_button = menu_button_kwargs["content"]
        actions: list[ft.Control] = [
            self.documents_container,
            ft.Container(**menu_button_kwargs),
        ]

        self.logo = ft.Container(
            **Style.app_logo(),
            on_click=self.go_home,
            visible=not show,
        )

        self.title_text = ft.Text(**Style.app_name(is_narrow))
        super().__init__(
            **Style.appbar(actions),
            leading=ft.Row(
                [
                    self.menu_icon,
                    self.logo,
                    ft.Container(
                        self.title_text,
                        on_click=self.go_home,
                    ),
                ],
            ),
        )

    # ── Document items ──────────────────────────────────────────────
    def set_documents(self, documents: list[str]):
        self.documents = documents or []
        new_kwargs = Style.documents_menu(
            self._build_document_items(), len(self.documents)
        )
        for key, value in new_kwargs.items():
            setattr(self.documents_container, key, value)
        self.documents_container.visible = bool(self.documents)
        self.documents_container.update()

    def _build_document_items(self) -> list[ft.PopupMenuItem]:
        items: list[ft.PopupMenuItem] = []
        for name in self.documents:
            items.append(
                ft.PopupMenuItem(
                    content=ft.Container(
                        **Style.doc_container(),
                        content=ft.Row(
                            [
                                ft.Icon(**Style.doc_icon()),
                                ft.Text(**Style.doc_title(name)),
                            ],
                        ),
                    ),
                )
            )
        return items

    # ── Menu items ──────────────────────────────────────────────────
    def _build_menu_items(self) -> list[ft.PopupMenuItem]:
        items: list[ft.PopupMenuItem] = []

        if self.user_email:
            items.append(
                ft.PopupMenuItem(
                    content=ft.Container(**Style.menu_item(self.user_email))
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
    def _on_sign_in(self):
        self.ref_page.run_task(self._sign_in)

    async def _sign_in(self):
        await self.ref_page.push_route("/login")

    def _on_sign_out(self):
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
        self.logo.visible = not visible
        new_style = Style.app_name(is_narrow=visible)["style"]
        self.title_text.style = new_style

    def _switch_theme(self):
        self.ref_page.theme_mode = (
            ft.ThemeMode.DARK
            if self.ref_page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.menu_button.items = self._build_menu_items()
        self.ref_page.update()

    async def go_home(self):
        await self.ref_page.push_route("/")
