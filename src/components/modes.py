import flet as ft

from utils import Config


class Modes(ft.Container):
    def __init__(self, is_mobile: bool = False):
        super().__init__()

        self.padding = ft.Padding.symmetric(
            horizontal=20, vertical=20 if is_mobile else 60
        )

        # Section Title and Subtitle
        title = ft.Text(
            "Choose Your Mode:",
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
            "EasyDoc AI offers flexible ways to interact with your documents based on your privacy and storage needs.",
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
                content=ft.Icon(icon_name, color=Config.PRIMARY, size=25),
                bgcolor=icon_bg_color,
                padding=15,
                border_radius=20,
                margin=ft.Margin.only(bottom=10),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            )

            card_title = ft.Text(
                step_title,
                size=18 if is_mobile else 22,
                weight=ft.FontWeight.W_600,
                # color=ft.Colors.ON_SURFACE,
                font_family=Config.FONT,
                text_align=ft.TextAlign.START,
                width=float("inf"),
            )

            card_desc = ft.Text(
                step_desc,
                size=13 if is_mobile else 14,
                color=ft.Colors.ON_SURFACE_VARIANT,
                font_family=Config.FONT,
                text_align=ft.TextAlign.START,
                width=float("inf"),
            )

            def on_card_hover(e):
                is_hovered = e.data

                # Fill the inner container with Primary on hover, clear on leave
                inner.bgcolor = Config.PRIMARY if is_hovered else None

                # Border for hover emphasis
                inner.border = (
                    ft.Border.all(1, Config.PRIMARY)
                    if is_hovered
                    else ft.Border.all(1, ft.Colors.TRANSPARENT)
                )

                # Invert text for contrast
                card_title.color = (
                    ft.Colors.WHITE if is_hovered else ft.Colors.ON_SURFACE
                )
                card_desc.color = (
                    ft.Colors.WHITE if is_hovered else ft.Colors.ON_SURFACE_VARIANT
                )

                # Invert the icon background so it pops on the fully filled card
                icon_container.bgcolor = (
                    ft.Colors.WHITE if is_hovered else icon_bg_color
                )
                icon_container.content.color = (
                    Config.PRIMARY if is_hovered else Config.PRIMARY
                )

                icon_container.update()
                card_title.update()
                card_desc.update()
                inner.update()

            inner = ft.Container(
                content=ft.Column(
                    [
                        icon_container,
                        card_title,
                        card_desc,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=20 if is_mobile else 35,
                border_radius=15,
                border=ft.Border.all(1, ft.Colors.TRANSPARENT),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            )

            card = ft.Card(
                elevation=10,
                bgcolor=Config.GREY_BG,
                content=inner,
            )

            # Wrap Card in a Container for hover — Card intercepts hover events
            # from its children, so we must handle hover at this outer level.
            return ft.Container(
                content=card,
                on_hover=lambda e: on_card_hover(e),
                # on_click=lambda _: None,
            )

        # Create the 3 cards
        card1 = create_card(
            ft.Icons.TIMER_OUTLINED,
            "Session Mode",
            "Documents are processed temporarily in your browser session. All data is cleared instantly upon refresh for maximum privacy.",
        )

        card2 = create_card(
            ft.Icons.CLOUD_OUTLINED,
            "Cloud Mode",
            "Create an account to save your documents and chat history securely in the cloud. Access your analysis anytime, anywhere.",
        )

        cards_row = ft.ResponsiveRow(
            [
                ft.Column(col={"sm": 12, "md": 6}, controls=[card1]),
                ft.Column(col={"sm": 12, "md": 6}, controls=[card2]),
            ],
            spacing=12 if is_mobile else 30,
            run_spacing=12 if is_mobile else 30,
        )

        self.content = ft.Column(
            [header_container, cards_row],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
