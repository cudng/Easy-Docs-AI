import flet as ft

from utils import Config


class Appbar(ft.AppBar):
    def __init__(self, page, margin_left: int, func):
        super().__init__(
            leading=ft.Row(
                [
                    ft.VerticalDivider(color=ft.Colors.TRANSPARENT, width=margin_left),
                    ft.Container(
                        ft.Image(Config.SVG, color="#13DAEC"),  # noqa
                        padding=ft.Padding.only(left=10, top=10, bottom=10),
                    ),
                    ft.Text(
                        "Easy Docs AI",
                        style=ft.TextStyle(
                            weight=ft.FontWeight.W_700,
                            font_family=Config.FONT,
                            size=20,
                            color="#13DAEC",
                        ),
                    ),
                ]
            ),
            toolbar_height=60,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LIGHT_MODE
                    if page.theme_mode == ft.ThemeMode.DARK
                    else ft.Icons.DARK_MODE,
                    tooltip="Theme",
                    margin=ft.Margin.only(right=20),
                    on_click=lambda e: func(e),
                ),
                ft.Button(
                    "Login",
                    bgcolor="#13DAEC",
                    color=ft.Colors.BLACK,
                    margin=ft.Margin.only(right=20),
                ),  # noqa
            ],
        )

    def update_margin(self, w: int):
        self.leading.controls[0].width = w
        self.update()
