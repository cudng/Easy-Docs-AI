import flet as ft

from utils import Config


class HowItWork(ft.Container):
    def __init__(self, is_mobile: bool = False):
        super().__init__()

        # Responsive spacing
        self.padding = ft.Padding.symmetric(
            horizontal=20, vertical=20 if is_mobile else 60
        )

        # Section Title and Subtitle
        title = ft.Text(
            "How It Works",
            style=ft.TextStyle(
                size=24 if is_mobile else 36,
                color=ft.Colors.ON_SURFACE,
                font_family=Config.FONT,
                weight=ft.FontWeight.BOLD,
            ),
            text_align=ft.TextAlign.CENTER,
            width=float("inf"),
        )

        subtitle = ft.Text(
            "Three simple steps to unlock the knowledge buried in your files. No complex\nsetup required.",
            style=ft.TextStyle(
                size=14 if is_mobile else 16,
                color=ft.Colors.ON_SURFACE_VARIANT,
                font_family=Config.FONT,
            ),
            text_align=ft.TextAlign.CENTER,
            width=float("inf"),
        )

        header_container = ft.Container(
            content=ft.Column(
                [title, subtitle], alignment=ft.MainAxisAlignment.CENTER, spacing=15
            ),
            margin=ft.Margin.only(bottom=24 if is_mobile else 50),
        )

        # Helper method to create cards
        def create_card(icon_name, step_title, step_desc):

            icon_bg_color = f"#26{Config.PRIMARY.lstrip('#')}"

            icon_container = ft.Container(
                content=ft.Icon(icon=icon_name, color=Config.PRIMARY, size=25),
                bgcolor=icon_bg_color,
                padding=15,
                border_radius=20,
                margin=ft.Margin.only(bottom=10),
            )

            return ft.Card(
                elevation=10,
                bgcolor=Config.GREY_BG,
                content=ft.Container(
                    content=ft.Column(
                        [
                            icon_container,
                            ft.Text(
                                step_title,
                                style=ft.TextStyle(
                                    size=18 if is_mobile else 20,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.ON_SURFACE,
                                    font_family=Config.FONT,
                                ),
                                text_align=ft.TextAlign.CENTER,
                                width=float("inf"),
                            ),
                            ft.Text(
                                step_desc,
                                style=ft.TextStyle(
                                    size=13 if is_mobile else 14,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                    font_family=Config.FONT,
                                ),
                                text_align=ft.TextAlign.CENTER,
                                width=float("inf"),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20 if is_mobile else 35,
                    border_radius=15,
                ),
            )

        # Create the 3 cards
        card1 = create_card(
            ft.Icons.CLOUD_UPLOAD_OUTLINED,
            "1. Upload Documents",
            "Drag and drop any PDF, DOCX, or TXT file. We support batch uploading for large knowledge bases.",
        )

        card2 = create_card(
            ft.Icons.AUTO_AWESOME,
            "2. Smart Analysis",
            "Our system instantly analyzes your data, creating connections to help find answers quickly.",
        )

        card3 = create_card(
            ft.Icons.CHAT_BUBBLE_OUTLINE,
            "3. Ask & Summarize",
            "Ask questions in natural language. Get accurate answers with direct citations to the source text.",
        )

        cards_row = ft.ResponsiveRow(
            [
                ft.Column(col={"sm": 12, "md": 4}, controls=[card1]),
                ft.Column(col={"sm": 12, "md": 4}, controls=[card2]),
                ft.Column(col={"sm": 12, "md": 4}, controls=[card3]),
            ],
            spacing=12 if is_mobile else 30,
            run_spacing=12 if is_mobile else 30,
        )

        self.content = ft.Column(
            [header_container, cards_row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
