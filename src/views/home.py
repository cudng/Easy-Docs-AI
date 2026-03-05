import flet as ft

from components import Appbar, Hero
from utils import Responsive


class HomePage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)

        self.responsive = Responsive()
        self.config = self.responsive.get_size()
        self.font_size = self.config["font_size"]
        self.left_margin = self.config["left_margin"]
        self.top_margin = self.config["top_margin"]
        self.top_divider = ft.Divider(
            color=ft.Colors.TRANSPARENT, height=self.top_margin
        )
        self.left_divider = ft.VerticalDivider(
            color=ft.Colors.TRANSPARENT, width=self.left_margin
        )
        self.appbar: Appbar = Appbar(page, self.font_size, self.switch_theme)
        self.hero = Hero(self.font_size)

        self.controls = [
            ft.Column([self.top_divider, ft.Row([self.left_divider, self.hero])])
        ]

        page.on_resize = self.on_resize

    def switch_theme(self, e):

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

    def on_resize(self, e):
        width = self.page.width

        if Responsive.crossed_breakpoint(width):
            config = self.responsive.get_size()
            font_size = config["font_size"]
            left_margin = config["left_margin"]
            self.hero.rebuild_shapes(font_size)
            self.appbar.update_margin(left_margin)
            self.page.update()
