import flet as ft

from utils import Responsive


class SessionMode(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route, scroll=ft.ScrollMode.HIDDEN)

        self.responsive = Responsive()
        self.config = self.responsive.get_size()

        self.controls = [ft.Text("Session Mode")]
