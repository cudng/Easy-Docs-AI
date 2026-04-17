import flet as ft

from components import Appbar, Footer
from utils import Config, Responsive


class PageNotFound(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)

        # ── Main Content ────────────────────────────────────────────
        self.error_icon = ft.Icon(
            ft.Icons.REPORT_GMAILERRORRED_ROUNDED, size=80, color=Config.ERROR
        )

        self.title = ft.Text(
            "404 - Page Not Found",
            size=36,
            weight=ft.FontWeight.W_700,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.subtitle = ft.Text(
            "Oops! We couldn't find the page you're looking for.",
            size=18,
            color=ft.Colors.OUTLINE,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.home_btn = ft.Button(
            "Back to Home",
            icon=ft.Icons.ARROW_BACK_ROUNDED,
            bgcolor=Config.PRIMARY,
            color=ft.Colors.BLACK,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=12),
                padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            ),
            on_click=lambda _: self.page.go("/"),
        )

        # ── Layout ──────────────────────────────────────────────────
        self.main_content = ft.Container(
            content=ft.Column(
                [
                    self.error_icon,
                    ft.Container(height=10),
                    self.title,
                    ft.Container(height=5),
                    self.subtitle,
                    ft.Container(height=30),
                    self.home_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(vertical=100, horizontal=20),
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

        self.controls = [
            self.main_content,
        ]
