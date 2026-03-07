import flet as ft

from utils import Config


class Footer(ft.Container):
    def __init__(self):
        super().__init__(
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            padding=ft.Padding.symmetric(vertical=40, horizontal=40),
            margin=ft.Margin.only(top=60),
            content=ft.Column(
                [
                    # ── Divider ──
                    ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=30),
                    # ── Bottom bar: copyright ──
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Image(Config.SVG, color="#13DAEC"),
                                        width=28,
                                        height=28,
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
                                ],
                                spacing=8,
                            ),
                            ft.Text(
                                "© 2026 Easy Docs AI. All rights reserved.",
                                style=ft.TextStyle(
                                    size=12,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                    font_family=Config.FONT,
                                ),
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "Author: Yevhen Kryvtsov",
                                        style=ft.TextStyle(
                                            weight=ft.FontWeight.W_700,
                                            size=14,
                                            font_family=Config.FONT,
                                        ),
                                        margin=ft.Margin.only(right=10),
                                    ),
                                    ft.IconButton(
                                        ft.Image(
                                            src="icons/telegram.svg",
                                            width=20,
                                            height=20,
                                            color="#26A5E4",
                                        ),
                                        tooltip="Telegram",
                                    ),
                                    ft.IconButton(
                                        ft.Image(
                                            src="icons/instagram.svg",
                                            width=20,
                                            height=20,
                                            color="#FF0069",
                                        ),
                                        tooltip="Instagram",
                                    ),
                                    ft.IconButton(
                                        ft.Image(
                                            src="icons/whatsapp.svg",
                                            width=20,
                                            height=20,
                                            color="#25D366",
                                        ),
                                        tooltip="WhatsApp",
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=20,
            ),
        )

    @staticmethod
    def _footer_link(label: str) -> ft.TextButton:
        return ft.TextButton(
            label,
            style=ft.ButtonStyle(
                color=ft.Colors.ON_SURFACE_VARIANT,
                padding=ft.Padding.all(0),
                text_style=ft.TextStyle(size=13, font_family=Config.FONT),
            ),
        )
