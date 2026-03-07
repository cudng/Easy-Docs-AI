import flet as ft

from utils import Config


class ChatMock(ft.Container):
    def __init__(self):
        super().__init__()

        # ── helpers ──────────────────────────────────────────────────
        _TEAL = Config.TEAL
        _TEAL_DARK = Config.TEAL_DARK
        _AI_PURPLE = Config.AI_PURPLE
        _GREY_BG = ft.Colors.SURFACE_CONTAINER_LOWEST
        _TEXT_MAIN = ft.Colors.ON_SURFACE
        _TEXT_MUTED = ft.Colors.with_opacity(0.55, ft.Colors.ON_SURFACE)
        _FONT = Config.FONT

        def _user_avatar():
            return ft.Container(
                width=28,
                height=28,
                border_radius=14,
                bgcolor="#C8A97E",
                content=ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.WHITE),
            )

        def _ai_avatar():
            return ft.Container(
                width=28,
                height=28,
                border_radius=14,
                bgcolor=_AI_PURPLE,
                content=ft.Icon(ft.Icons.SMART_TOY, size=16, color=ft.Colors.WHITE),
            )

        def _user_bubble(text: str):
            return ft.Row(
                [
                    ft.Container(expand=True),
                    ft.Container(
                        padding=ft.Padding.all(10),
                        border_radius=ft.BorderRadius(14, 14, 2, 14),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0),
                            end=ft.Alignment(1, 0),
                            colors=[_TEAL, _TEAL_DARK],
                        ),
                        content=ft.Text(
                            text,
                            color=ft.Colors.WHITE,
                            size=11,
                            font_family=_FONT,
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        width=220,
                    ),
                    _user_avatar(),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        def _ai_message():
            source_chip = ft.Container(
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                border_radius=8,
                border=ft.Border.all(
                    1, ft.Colors.with_opacity(0.15, ft.Colors.ON_SURFACE)
                ),
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=13, color=_TEAL),
                        ft.Text(
                            "1 Source Found", size=10, color=_TEAL, font_family=_FONT
                        ),
                        ft.Container(expand=True),
                        ft.Icon(
                            ft.Icons.KEYBOARD_ARROW_DOWN, size=14, color=_TEXT_MUTED
                        ),
                    ],
                    spacing=4,
                ),
            )

            action_row = ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.COPY_OUTLINED, size=12, color=_TEXT_MUTED),
                            ft.Text(
                                "Copy", size=10, color=_TEXT_MUTED, font_family=_FONT
                            ),
                        ],
                        spacing=3,
                    ),
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.THUMB_UP_ALT_OUTLINED,
                                size=12,
                                color=_TEXT_MUTED,
                            ),
                            ft.Text(
                                "Helpful", size=10, color=_TEXT_MUTED, font_family=_FONT
                            ),
                        ],
                        spacing=3,
                    ),
                    ft.Icon(
                        ft.Icons.THUMB_DOWN_ALT_OUTLINED, size=12, color=_TEXT_MUTED
                    ),
                ],
                spacing=10,
            )

            bubble = ft.Container(
                padding=ft.Padding.all(10),
                border_radius=ft.BorderRadius(2, 14, 14, 14),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                content=ft.Text(
                    "In Q3, the primary revenue drivers were the expansion of the enterprise cloud segment and a 15% increase in subscription renewals.",
                    size=10,
                    color=_TEXT_MAIN,
                    font_family=_FONT,
                    max_lines=5,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                width=250,
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            _ai_avatar(),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "AI Assistant",
                                                size=10,
                                                weight=ft.FontWeight.W_600,
                                                color=_TEXT_MAIN,
                                                font_family=_FONT,
                                            ),
                                            ft.Text(
                                                "· Just now",
                                                size=9,
                                                color=_TEXT_MUTED,
                                                font_family=_FONT,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    bubble,
                                    source_chip,
                                    action_row,
                                ],
                                spacing=5,
                                tight=True,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                tight=True,
            )

        def _typing_indicator():
            return ft.Row(
                [
                    _ai_avatar(),
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                        border_radius=ft.BorderRadius(2, 14, 14, 14),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        content=ft.Row(
                            [
                                ft.Container(
                                    width=5,
                                    height=5,
                                    border_radius=3,
                                    bgcolor=_TEXT_MUTED,
                                ),
                                ft.Container(
                                    width=5,
                                    height=5,
                                    border_radius=3,
                                    bgcolor=_TEXT_MUTED,
                                ),
                                ft.Container(
                                    width=5,
                                    height=5,
                                    border_radius=3,
                                    bgcolor=_TEXT_MUTED,
                                ),
                            ],
                            spacing=3,
                        ),
                    ),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        def _input_bar():
            return ft.Container(
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                border_radius=20,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                shadow=ft.BoxShadow(
                    blur_radius=6, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
                ),
                content=ft.Row(
                    [
                        ft.Text(
                            "Ask anything about the document...",
                            size=10,
                            color=_TEXT_MUTED,
                            font_family=_FONT,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.TUNE, size=14, color=_TEXT_MUTED),
                        ft.Container(width=6),
                        ft.Container(
                            width=26,
                            height=26,
                            border_radius=13,
                            gradient=ft.LinearGradient(
                                begin=ft.Alignment(-1, 0),
                                end=ft.Alignment(1, 0),
                                colors=[_TEAL, _TEAL_DARK],
                            ),
                            content=ft.Icon(
                                ft.Icons.ARROW_UPWARD, size=14, color=ft.Colors.WHITE
                            ),
                            alignment=ft.Alignment.CENTER,
                        ),
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

        # ── fight_container (chat mock) ───────────────────────────────
        self.content = ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE),
            content=ft.Column(
                [
                    # date separator
                    ft.Row(
                        [
                            ft.Container(
                                padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                content=ft.Text(
                                    "Today, October 24th",
                                    size=9,
                                    color=_TEXT_MUTED,
                                    font_family=_FONT,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    _user_bubble(
                        "Summarize the key revenue drivers mentioned in the third quarter report."
                    ),
                    _ai_message(),
                    _user_bubble("What about the churn rate?"),
                    _typing_indicator(),
                    _input_bar(),
                ],
                spacing=10,
            ),
        )
