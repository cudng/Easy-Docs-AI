import flet as ft


class Style:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def left_divider(self) -> dict:
        width: int = self.page.width
        print(width)
        return {
            "width": 10 if width < 600 else 20 if width < 1200 else 40,
        }

    def hero_title_size(self) -> dict:
        width: int = self.page.width
        return {"size": 50 if width < 600 else 25}
