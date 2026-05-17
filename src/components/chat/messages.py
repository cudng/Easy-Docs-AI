import flet as ft

from utils import Config


class UserMessage(ft.Container):
    def __init__(self, text: str):
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "You",
                                size=11,
                                color=ft.Colors.OUTLINE,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    text,
                                    color=ft.Colors.ON_PRIMARY,
                                    size=15,
                                    selectable=True,
                                ),
                                bgcolor=Config.PRIMARY,
                                padding=ft.Padding.symmetric(
                                    horizontal=20, vertical=14
                                ),
                                border_radius=ft.BorderRadius.only(
                                    top_left=16,
                                    bottom_left=16,
                                    bottom_right=16,
                                    top_right=2,
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.PERSON, color=ft.Colors.OUTLINE, size=20
                        ),
                        width=32,
                        height=32,
                        border_radius=16,
                        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                        alignment=ft.Alignment.CENTER,
                        margin=ft.Margin.only(top=20),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.Padding.only(left=60),
            expand=True,
        )


class AiMessage(ft.Container):
    def __init__(self, text: str = ""):
        super().__init__(padding=ft.Padding.only(right=60), expand=True)

        self.text_widget = ft.Text(
            text,
            color=ft.Colors.ON_SURFACE,
            size=15,
            selectable=True,
        )

        self.bubble = ft.Container(
            content=self.text_widget,
            bgcolor=ft.Colors.SURFACE,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            border_radius=ft.BorderRadius.only(
                top_left=2,
                bottom_left=16,
                bottom_right=16,
                top_right=16,
            ),
        )

        self.action_buttons = ft.Row(
            controls=[
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CONTENT_COPY, size=14),
                            ft.Text("Copy", size=12),
                        ],
                        spacing=4,
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.OUTLINE,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    ),
                ),
            ],
            spacing=4,
        )

        self.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.WHITE, size=18),
                    width=32,
                    height=32,
                    border_radius=16,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[ft.Colors.INDIGO_500, ft.Colors.PURPLE_600],
                    ),
                    alignment=ft.Alignment.CENTER,
                    margin=ft.Margin.only(top=20),
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Text(
                                    "AI Assistant",
                                    size=11,
                                    color=ft.Colors.OUTLINE,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Text("•", size=11, color=ft.Colors.OUTLINE_VARIANT),
                                ft.Text(
                                    "Just now",
                                    size=11,
                                    color=ft.Colors.OUTLINE_VARIANT,
                                ),
                            ],
                            spacing=6,
                        ),
                        self.bubble,
                        self.action_buttons,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def set_text(self, text: str):
        self.text_widget.value = text

    def append_text(self, chunk: str):
        self.text_widget.value = (self.text_widget.value or "") + chunk


class Loading(ft.Container):
    def __init__(self):
        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SMART_TOY, color=ft.Colors.WHITE, size=18
                        ),
                        width=32,
                        height=32,
                        border_radius=16,
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_LEFT,
                            end=ft.Alignment.BOTTOM_RIGHT,
                            colors=[ft.Colors.INDIGO_500, ft.Colors.PURPLE_600],
                        ),
                        alignment=ft.Alignment.CENTER,
                        margin=ft.Margin.only(top=10),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.ProgressRing(
                                    width=16,
                                    height=16,
                                    stroke_width=2,
                                    color=ft.Colors.OUTLINE,
                                )
                            ]
                        ),
                        bgcolor=ft.Colors.SURFACE,
                        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                        border_radius=ft.BorderRadius.only(
                            top_left=2, bottom_left=16, bottom_right=16, top_right=16
                        ),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.Padding.only(right=60),
        )
