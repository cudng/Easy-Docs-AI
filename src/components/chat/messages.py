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
                                    text, color=ft.Colors.ON_PRIMARY, size=15
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
                                shadow=ft.BoxShadow(
                                    blur_radius=4,
                                    color=ft.Colors.with_opacity(0.1, ft.Colors.SHADOW),
                                    offset=ft.Offset(0, 2),
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
    def __init__(self, text: str):
        super().__init__(padding=ft.Padding.only(right=60))

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
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.THUMB_UP, size=14),
                            ft.Text("Helpful", size=12),
                        ],
                        spacing=4,
                    ),
                    style=ft.ButtonStyle(
                        color=ft.Colors.OUTLINE,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    ),
                ),
                ft.TextButton(
                    content=ft.Row([ft.Icon(ft.Icons.THUMB_DOWN, size=14)], spacing=0),
                    style=ft.ButtonStyle(
                        color=ft.Colors.OUTLINE,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    ),
                ),
            ],
            spacing=4,
        )

        # Source Accordion using ExpansionTile
        self.source_accordion = ft.ExpansionTile(
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.MENU_BOOK, color=Config.PRIMARY, size=18),
                    ft.Text(
                        "1 Source Found",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=Config.PRIMARY,
                    ),
                ],
                spacing=8,
            ),
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "PAGE 4, PARAGRAPH 2",
                                        size=10,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "High Confidence",
                                            size=10,
                                            color=Config.PRIMARY,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                        bgcolor=ft.Colors.with_opacity(
                                            0.1, Config.PRIMARY
                                        ),
                                        padding=ft.Padding.symmetric(
                                            horizontal=8, vertical=2
                                        ),
                                        border_radius=10,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                '"...Enterprise cloud segment revenue grew by 25% YoY, driven largely by new client acquisitions in the fintech sector. Furthermore, subscription renewals saw a 15% uplift following the Q2 feature rollout..."',
                                italic=True,
                                size=13,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=16,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                    margin=ft.Margin.only(bottom=8),
                )
            ],
            collapsed_text_color=ft.Colors.ON_SURFACE,
            text_color=ft.Colors.ON_SURFACE,
            shape=ft.RoundedRectangleBorder(radius=12),
            collapsed_shape=ft.RoundedRectangleBorder(radius=12),
        )

        self.source_container = ft.Container(
            content=self.source_accordion,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=12,
            bgcolor=ft.Colors.SURFACE,
            width=400,
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
                        ft.Container(
                            content=ft.Text(text, color=ft.Colors.ON_SURFACE, size=15),
                            bgcolor=ft.Colors.SURFACE,
                            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                            border_radius=ft.BorderRadius.only(
                                top_left=2,
                                bottom_left=16,
                                bottom_right=16,
                                top_right=16,
                            ),
                            shadow=ft.BoxShadow(
                                blur_radius=4,
                                color=ft.Colors.with_opacity(0.1, ft.Colors.SHADOW),
                                offset=ft.Offset(0, 2),
                            ),
                        ),
                        self.source_container,
                        self.action_buttons,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

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
                                # Simulated bouncing effect natively supported? We can use ProgressRing or simulate typing
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
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
