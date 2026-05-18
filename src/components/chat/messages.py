import flet as ft

from utils import Config


class UserMessage(ft.Container):
    def __init__(self, text: str, is_narrow: bool = False):
        avatar_size = 24 if is_narrow else 32
        avatar_radius = avatar_size // 2
        icon_size = 14 if is_narrow else 20
        label_size = 11
        body_size = 13 if is_narrow else 15
        bubble_h = 14 if is_narrow else 20
        bubble_v = 10 if is_narrow else 14
        outer_left = 20 if is_narrow else 60
        avatar_top = 14 if is_narrow else 20

        super().__init__(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "You",
                                size=label_size,
                                color=ft.Colors.OUTLINE,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    text,
                                    color=ft.Colors.ON_PRIMARY,
                                    size=body_size,
                                    selectable=True,
                                ),
                                bgcolor=Config.PRIMARY,
                                padding=ft.Padding.symmetric(
                                    horizontal=bubble_h, vertical=bubble_v
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
                            ft.Icons.PERSON, color=ft.Colors.OUTLINE, size=icon_size
                        ),
                        width=avatar_size,
                        height=avatar_size,
                        border_radius=avatar_radius,
                        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                        alignment=ft.Alignment.CENTER,
                        margin=ft.Margin.only(top=avatar_top),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.Padding.only(left=outer_left),
            expand=True,
        )


class AiMessage(ft.Container):
    def __init__(self, text: str = "", is_narrow: bool = False):
        avatar_size = 24 if is_narrow else 32
        avatar_radius = avatar_size // 2
        icon_size = 14 if is_narrow else 18
        label_size = 11
        body_size = 13 if is_narrow else 15
        bubble_h = 14 if is_narrow else 24
        bubble_v = 10 if is_narrow else 16
        outer_right = 20 if is_narrow else 60
        avatar_top = 14 if is_narrow else 20
        action_icon_size = 12 if is_narrow else 14
        action_text_size = 11 if is_narrow else 12

        super().__init__(padding=ft.Padding.only(right=outer_right), expand=True)

        self.text_widget = ft.Text(
            text,
            color=ft.Colors.ON_SURFACE,
            size=body_size,
            selectable=True,
        )

        self.bubble = ft.Container(
            content=self.text_widget,
            bgcolor=ft.Colors.SURFACE,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            padding=ft.Padding.symmetric(horizontal=bubble_h, vertical=bubble_v),
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
                            ft.Icon(ft.Icons.CONTENT_COPY, size=action_icon_size),
                            ft.Text("Copy", size=action_text_size),
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
                    content=ft.Icon(
                        ft.Icons.SMART_TOY, color=ft.Colors.WHITE, size=icon_size
                    ),
                    width=avatar_size,
                    height=avatar_size,
                    border_radius=avatar_radius,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[ft.Colors.INDIGO_500, ft.Colors.PURPLE_600],
                    ),
                    alignment=ft.Alignment.CENTER,
                    margin=ft.Margin.only(top=avatar_top),
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Text(
                                    "AI Assistant",
                                    size=label_size,
                                    color=ft.Colors.OUTLINE,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Text(
                                    "•", size=label_size, color=ft.Colors.OUTLINE_VARIANT
                                ),
                                ft.Text(
                                    "Just now",
                                    size=label_size,
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
