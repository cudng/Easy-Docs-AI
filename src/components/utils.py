import flet as ft

from utils import Config


def create_placeholder():
    return ft.Container(
        content=ft.Text(
            "AI can make mistakes. Please verify important information.",
            size=11,
            color=ft.Colors.OUTLINE,
        ),
        margin=ft.Margin.only(top=12),
    )


class AccountMenu(ft.Container):
    """Avatar trigger with a custom floating dropdown (no ugly square ripple)."""

    DROPDOWN_WIDTH = 260

    def __init__(self, page: ft.Page, email: str, on_sign_out):
        self.page_ref = page
        self.email = email
        self.on_sign_out_cb = on_sign_out
        self.is_open = False

        initial = (email[:1] or "?").upper()

        self.avatar = ft.Container(
            content=ft.CircleAvatar(
                content=ft.Text(
                    initial,
                    size=14,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.WHITE,
                    font_family=Config.FONT,
                ),
                bgcolor=Config.PRIMARY,
                radius=18,
            ),
            on_click=self._toggle,
            tooltip=email,
            border_radius=18,
            ink=False,
        )

        self.sign_out_item = ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=8,
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGOUT, size=18, color=Config.ERROR),
                    ft.Text(
                        "Sign Out",
                        size=14,
                        color=Config.ERROR,
                        font_family=Config.FONT,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=12,
            ),
            on_click=self._handle_sign_out,
            on_hover=self._hover_sign_out,
        )

        self.dropdown = ft.Container(
            visible=False,
            top=10,
            right=10,
            width=self.DROPDOWN_WIDTH,
            padding=ft.Padding.all(6),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            border_radius=12,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, Config.PRIMARY)),
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.15, ft.Colors.SHADOW),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                [
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Signed in as",
                                    size=11,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                                ft.Text(
                                    email,
                                    size=13,
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
                    ft.Divider(
                        height=1,
                        color=ft.Colors.with_opacity(0.1, Config.PRIMARY),
                    ),
                    self.sign_out_item,
                ],
                spacing=4,
                tight=True,
            ),
        )

        # Transparent layer that closes the dropdown on outside click
        self.backdrop = ft.Container(
            visible=False,
            expand=True,
            on_click=self._close,
            bgcolor=ft.Colors.TRANSPARENT,
        )

        # Register overlay controls once
        page.overlay.append(self.backdrop)
        page.overlay.append(self.dropdown)

        super().__init__(
            content=self.avatar,
            margin=ft.Margin.only(right=40),
        )

    # ── Interaction ─────────────────────────────────────────────────
    def _toggle(self, e=None):
        self.is_open = not self.is_open
        self.dropdown.visible = self.is_open
        self.backdrop.visible = self.is_open
        self.page_ref.update()

    def _close(self, e=None):
        self.is_open = False
        self.dropdown.visible = False
        self.backdrop.visible = False
        self.page_ref.update()

    def _handle_sign_out(self, e=None):
        self._close()
        if self.on_sign_out_cb:
            self.on_sign_out_cb(e)

    def _hover_sign_out(self, e):
        e.control.bgcolor = (
            ft.Colors.with_opacity(0.08, Config.ERROR) if e.data == "true" else None
        )
        e.control.update()


# class LeftDivider(ft.Container):
#     def did_mount(self):
#         self.width = self._get_thickness()
#         self.bgcolor = ft.Colors.GREY_300
#         self.page.on_resize = self._on_resize
#         self.update()
#
#     def _get_thickness(self):
#         if self.page.width < 600:
#             return 20
#         elif self.page.width < 1200:
#             return 50
#         return 100
#
#     def _on_resize(self, e):
#         self.width = self._get_thickness()
#         self.update()
#
#
# # utils.py
# def register_resize(page: ft.Page, callback):
#     existing = page.on_resize
#
#     def handler(e):
#         if existing:
#             existing(e)
#         callback(e)
#
#     page.on_resize = handler
