import uuid

import flet as ft

from components import Appbar
from utils import Config, Responsive


class SessionMode(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route, scroll=ft.ScrollMode.HIDDEN)

        self.responsive = Responsive()
        self.config = self.responsive.get_size()
        self.left_margin = self.config["left_margin"]

        # ── Appbar ──────────────────────────────────────────────────
        self.appbar: Appbar = Appbar(page, self.left_margin)

        self.page_ref = page

        # ── Upload-zone visuals ─────────────────────────────────────
        self.upload_icon = ft.Icon(
            ft.Icons.CLOUD_UPLOAD_OUTLINED,
            size=64,
            color=Config.PRIMARY,
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        self.drop_title = ft.Text(
            "Upload your document",
            size=22,
            weight=ft.FontWeight.W_600,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.subtitle_top = ft.Text(
            "Click anywhere in this area or use the button below",
            size=14,
            color=ft.Colors.OUTLINE,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.pick_btn = ft.Button(
            "Pick a File",
            icon=ft.Icons.FOLDER_OPEN,
            bgcolor=Config.PRIMARY,
            color=ft.Colors.BLACK,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=12),
            ),
            on_click=self._on_pick_click,
        )

        self.subtitle = ft.Text(
            "Supported formats: PDF, DOCX, TXT",
            size=13,
            color=ft.Colors.OUTLINE,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        # ── Inner content column ────────────────────────────────────
        self.inner_column = ft.Column(
            [
                self.upload_icon,
                self.drop_title,
                self.subtitle_top,
                ft.Container(height=4),
                self.pick_btn,
                ft.Container(height=4),
                self.subtitle,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # ── Upload zone inner padding ───────────────────────────────
        self.upload_zone = ft.Container(
            padding=ft.Padding.symmetric(horizontal=40, vertical=60),
            content=self.inner_column,
            border_radius=12,
        )

        # ── Card with elevation ─────────────────────────────────────
        self.upload_zone_card = ft.Card(
            content=self.upload_zone,
            elevation=10,
        )

        # ── Outer clickable wrapper ─────────────────────────────────
        # This container constrains width, centers the card,
        # handles click → file picker, and hover animation.
        self.card_wrapper = ft.Container(
            content=self.upload_zone_card,
            width=700,
            alignment=ft.Alignment.CENTER,
            border_radius=12,
            on_click=self._on_pick_click,
            on_hover=self._on_zone_hover,
            ink=True,
        )

        # ── Page layout ─────────────────────────────────────────────
        self.controls = [
            ft.Container(
                content=self.card_wrapper,
                expand=True,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(horizontal=20, vertical=40),
            ),
        ]

        page.on_resize = self._on_resize

    # ── Hover effect on card area ───────────────────────────────────
    def _on_zone_hover(self, e):
        is_hovered = e.data
        self.upload_zone.bgcolor = (
            ft.Colors.SURFACE_CONTAINER_LOWEST if is_hovered else None
        )

    # ── Pick file handler (async) ───────────────────────────────────
    async def _on_pick_click(self):
        result = await self.page_ref.file_picker.pick_files(  # noqa
            dialog_title="Choose a document",
            allowed_extensions=["pdf", "docx", "txt"],
            allow_multiple=True,
        )

        if result and len(result) > 0:
            
            print(f"Selected file: {result}")
            print(f"Selected file name: {result[0].name}")
            selected = result[0]
            
            # Use a globally unique identifier for this document
            doc_id = uuid.uuid4().hex
            
            self.page_ref.session.store.set(f"uploaded_file_{doc_id}", selected.name)
            await self.page_ref.push_route(f"/session/chat/{doc_id}")

    # ── Responsive resize ───────────────────────────────────────────
    def _on_resize(self):
        width: int = self.page_ref.width

        if width < 600:
            self.card_wrapper.width = width * 0.92
            self.upload_zone.padding = ft.Padding.symmetric(horizontal=20, vertical=40)
            self.drop_title.size = 18
        elif width < 1200:
            self.card_wrapper.width = min(600, int(width * 0.7))
            self.upload_zone.padding = ft.Padding.symmetric(horizontal=30, vertical=50)
            self.drop_title.size = 20
        else:
            self.card_wrapper.width = 700
            self.upload_zone.padding = ft.Padding.symmetric(horizontal=40, vertical=60)
            self.drop_title.size = 22

        if Responsive.crossed_breakpoint(width):
            config = self.responsive.get_size()
            self.appbar.update_margin(config["left_margin"])
