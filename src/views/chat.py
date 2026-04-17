import time

import flet as ft

from components import Appbar
from components.chat import AiMessage, Loading, UserMessage
from components.utils import create_placeholder
from utils import Config, Responsive, Style


class ChatPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        # Extract doc_id from the route: /session/chat/<doc_id>
        route_parts = self.page_ref.route.split("/")
        self.doc_id = route_parts[-1] if len(route_parts) > 3 else "default"

        self.uploaded_file = self.page_ref.session.store.get(
            f"uploaded_file_{self.doc_id}"
        )

        if not self.uploaded_file:
            self._build_no_document_view()
            return

        self.filename = self.uploaded_file.split("/")[-1]

        self.config = Responsive().get_size()
        self.left_margin = self.config["left_margin"]
        self.list_padding = self.config["list_padding"]
        self.sources_visible = True
        self.appbar: Appbar = Appbar(
            page=self.page_ref,
            filename=self.filename,
            margin_left=self.left_margin,
            on_toggle_sources=self._on_toggle_sources,
            chat_mode=True,
        )
        # 1. State / Memory
        self.chat_history_data = (
            self.page_ref.session.store.get(f"history_{self.doc_id}") or []
        )

        # 2. Main Layout Components
        self._build_chat_history()
        self._build_input_area()

        # 3. Main Container
        self.main_column = ft.Column(
            controls=[
                self.chat_listview,
            ],
            expand=True,
            scroll=None,
        )

        # Build View controls
        self.controls = [
            ft.Container(
                content=ft.Stack(
                    [
                        self.main_column,
                        ft.Container(
                            content=self.input_container,
                            alignment=ft.Alignment.BOTTOM_CENTER,
                            bottom=0,
                            left=0,
                            right=0,
                        ),
                    ],
                    expand=True,
                ),
                expand=True,
            ),
        ]

        page.on_resize = self._on_resize

    # --- No Document Safeguard ---
    def _build_no_document_view(self):
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.DESCRIPTION_OUTLINED,
                            size=64,
                            color=ft.Colors.OUTLINE,
                        ),
                        ft.Text(
                            "No document selected",
                            size=20,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.ON_SURFACE,
                        ),
                        ft.Text(
                            "Please go back and choose a document first.",
                            size=14,
                            color=ft.Colors.OUTLINE,
                        ),
                        ft.Container(height=16),
                        ft.Button(
                            "Go Back",
                            icon=ft.Icons.ARROW_BACK,
                            bgcolor=Config.PRIMARY,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda _: self.page_ref.go("/session"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                expand=True,
                alignment=ft.Alignment.CENTER,
            ),
        ]

    # --- Chat History ---
    def _build_chat_history(self):
        # We need padding at the bottom so the sticky input doesn't hide the last messages
        self.chat_listview = ft.ListView(
            **Style.chat_history(),
            padding=ft.Padding.only(
                top=32, bottom=160, left=self.list_padding, right=self.list_padding
            ),
        )

        for msg in self.chat_history_data:
            if msg["role"] == "user":
                self.chat_listview.controls.append(UserMessage(msg["content"]))

            elif msg["role"] == "ai":
                self.chat_listview.controls.append(
                    AiMessage(msg["content"], sources_visible=self.sources_visible)
                )

    # --- Input Area ---
    def _build_input_area(self):
        self.send_icon = ft.IconButton(
            **Style.send_button_icon(),
            on_click=self._handle_send,
            disabled=True,
            opacity=0.4,
        )

        self.input_field = ft.TextField(
            **Style.input_field(),
            on_submit=self._handle_send,
            on_change=self._on_input_change,
        )

        self.send_button = ft.Container(
            height=40,
            width=40,
            content=self.send_icon,
        )

        input_row = ft.Container(
            **Style.input_row(),
            content=ft.Row(
                controls=[
                    self.input_field,
                    ft.Container(
                        content=ft.Row(
                            [
                                self.send_button,
                            ]
                        ),
                        padding=ft.Padding.only(right=12, bottom=6),
                        alignment=ft.Alignment.BOTTOM_RIGHT,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
        )

        self.input_container = ft.Container(
            **Style.input_container(),
            content=ft.Column(
                [
                    ft.Container(
                        content=input_row,
                        width=900,
                    ),
                    create_placeholder(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # --- Input State ---
    def _on_input_change(self):
        has_text = bool(self.input_field.value and not self.input_field.value.isspace())
        self.send_icon.disabled = not has_text
        self.send_icon.opacity = 1.0 if has_text else 0.4
        self.send_icon.update()

    # --- Message Handling ---
    def _handle_send(self):
        text = self.input_field.value
        if not text or text.isspace():
            return

        self.input_field.value = ""
        self.send_icon.disabled = True
        self.send_icon.opacity = 0.4
        self.input_field.update()
        self.send_icon.update()

        # Add a user message
        self._add_user_message(text)

        # Add loading state
        self._show_loading()

        # Simulate AI processing (replace with actual RAG logic later)
        text_copy = text

        def _process():
            time.sleep(1.5)
            self._remove_loading()
            self._add_ai_message(
                f"This is a simulated response to: '{text_copy}'. Document processing logic will go here."
            )

        import threading

        threading.Thread(target=_process).start()

    def _add_user_message(self, text: str):
        bubble = UserMessage(text)
        self.chat_listview.controls.append(bubble)
        self.chat_listview.update()

        self.chat_history_data.append({"role": "user", "content": text})
        self.page_ref.session.store.set(
            f"history_{self.doc_id}", self.chat_history_data
        )

    def _add_ai_message(self, text: str):
        bubble = AiMessage(text, sources_visible=self.sources_visible)
        self.chat_listview.controls.append(bubble)
        self.chat_listview.update()

        self.chat_history_data.append({"role": "ai", "content": text})
        self.page_ref.session.store.set(
            f"history_{self.doc_id}", self.chat_history_data
        )

    def _show_loading(self):
        # Create 3 bouncing dots for loading animation
        self.loading_indicator = Loading()
        self.chat_listview.controls.append(self.loading_indicator)
        self.chat_listview.update()

    def _remove_loading(self):
        if (
            hasattr(self, "loading_indicator")
            and self.loading_indicator in self.chat_listview.controls
        ):
            self.chat_listview.controls.remove(self.loading_indicator)
            self.chat_listview.update()

    # --- Sources Toggle ---
    def _on_toggle_sources(self, visible: bool):
        self.sources_visible = visible
        for control in self.chat_listview.controls:
            if isinstance(control, AiMessage):
                control.set_sources_visible(visible)
        self.chat_listview.update()

    # --- Responsive logic ---
    def _on_resize(self):
        width = self.page_ref.width

        if Responsive.crossed_breakpoint(width):
            config = Responsive.get_size()
            padding = config["list_padding"]
            self.appbar.update_margin(config["left_margin"])
            self.chat_listview.padding = ft.Padding.only(
                top=32, bottom=160, left=padding, right=padding
            )

        self.appbar.update()
        self.chat_listview.update()

    async def go_back(self):
        await self.page_ref.push_route("/session")
