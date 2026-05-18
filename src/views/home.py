import flet as ft

from components import Appbar, Footer, Hero, HowItWork, Modes
from utils import Responsive, ScreenSize, get_user


class HomePage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route, scroll=ft.ScrollMode.HIDDEN)

        self.responsive = Responsive()
        self.config = self.responsive.get_size(page.width)
        self.font_size = self.config["font_size"]
        self.left_margin = self.config["left_margin"]
        self.top_margin = self.config["top_margin"]
        is_mobile = Responsive._last_breakpoint == ScreenSize.MOBILE
        self.top_divider = ft.Divider(
            color=ft.Colors.TRANSPARENT, height=self.top_margin
        )

        user = get_user(page)
        self.appbar: Appbar = Appbar(
            page,
            user_email=user["email"] if user else None,
        )
        self.hero = Hero(self.font_size)
        self.how_it_work = HowItWork(is_mobile=is_mobile)
        self.modes = Modes(is_mobile=is_mobile)
        self.footer = Footer(is_mobile=is_mobile)

        self.controls = [
            ft.Column(
                [
                    self.top_divider,
                    ft.Row([self.hero]),
                    ft.Divider(height=10 if is_mobile else 40),
                    self.how_it_work,
                    self.modes,
                    self.footer,
                ],
            )
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

    def on_resize(self):
        width = self.page.width
        if not width:
            return
        if Responsive.crossed_breakpoint(width):
            config = self.responsive.get_size()

            font_size = config["font_size"]
            top_margin = config["top_margin"]

            self.top_divider.height = top_margin
            self.top_divider.update()
            self.hero.rebuild_shapes(font_size)
