import asyncio
import uuid

import flet as ft

from components import Appbar, ChatDrawer, UploadCard
from components.chat import AiMessage, Loading, UserMessage
from components.utils import create_placeholder
from utils import (
    Responsive,
    Style,
    get_chat_documents,
    get_messages,
    get_user,
    insert_message,
    update_chat_title,
)
from utils.utils import Breakpoint


class ChatPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        user = get_user(page)
        self.is_logged_in = user is not None

        # Routes: /chat or /chat/<chat_id>
        route_parts = page.route.split("/")
        raw_chat_id = (
            route_parts[2] if len(route_parts) > 2 and route_parts[2] else None
        )
        if raw_chat_id is not None:
            try:
                self.chat_id: str | None = str(uuid.UUID(raw_chat_id))
            except (ValueError, TypeError):
                self.controls = []
                page.run_task(self._redirect_to_root)
                return
        else:
            self.chat_id = None

        self.config = Responsive().get_size()
        self.left_margin = self.config["left_margin"]
        self.list_padding = self.config["list_padding"]

        self.uploaded_files: list[str] = []
        self.chat_history_data: list[dict] = []

        if self.chat_id is not None:
            if self.is_logged_in:
                try:
                    doc_rows = get_chat_documents(self.chat_id)
                    self.uploaded_files = [d["file_name"] for d in doc_rows]
                    db_messages = get_messages(self.chat_id)
                    self.chat_history_data = [
                        {"sender": m["sender"], "content": m["content"]}
                        for m in db_messages
                    ]
                except Exception as err:
                    print(f"Error fetching chat data: {err}")
                    self.uploaded_files = []
                    self.chat_history_data = []
            else:
                self.uploaded_files = (
                    self.page_ref.session.store.get(f"uploaded_files_{self.chat_id}")
                    or []
                )
                self.chat_history_data = (
                    self.page_ref.session.store.get(f"history_{self.chat_id}") or []
                )

            if (
                not isinstance(self.uploaded_files, list)
                or not self.uploaded_files
                or not all(isinstance(x, str) for x in self.uploaded_files)
            ):
                self.controls = []
                page.run_task(self._redirect_to_root)
                return

        is_narrow = (page.width or 1200) < Breakpoint.MOBILE_BREAKPOINT

        self.appbar: Appbar = Appbar(
            page=page,
            margin_left=self.left_margin,
            user_email=user["email"] if user else None,
            documents=self.uploaded_files,
            on_menu_click=self._toggle_drawer,
            show_menu_icon=is_narrow,
        )

        self.drawer = ChatDrawer(page, self.chat_id, self.is_logged_in)
        self.drawer.visible = not is_narrow

        if self.chat_id is None:
            self.upload_card: UploadCard | None = UploadCard(
                page, on_chat_created=self._on_chat_created
            )
            right_pane = self.upload_card
        else:
            self.upload_card = None
            self._build_chat_history()
            self._build_input_area()
            self.main_column = ft.Column(
                controls=[self.chat_listview],
                expand=True,
                scroll=None,
            )
            right_pane = ft.Container(
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
            )

        self.controls = [
            ft.Row(
                [
                    self.drawer,
                    ft.Container(content=right_pane, expand=True),
                ],
                expand=True,
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ]

        page.on_resize = self._on_resize

    # --- Redirect / navigation helpers ---
    async def _redirect_to_root(self):
        self.page_ref.show_dialog(
            ft.SnackBar(
                content=ft.Text("Chat not found. Start a new chat."),
            )
        )
        await self.page_ref.push_route("/chat")

    async def _on_chat_created(self, chat_id: str):
        await self.page_ref.push_route(f"/chat/{chat_id}")

    # --- Drawer toggle (mobile hamburger) ---
    def _toggle_drawer(self, _e=None):
        self.drawer.visible = not self.drawer.visible
        self.drawer.update()

    # --- Chat history ---
    def _build_chat_history(self):
        self.chat_listview = ft.ListView(
            **Style.chat_history(),
            padding=ft.Padding.only(
                top=32, bottom=160, left=self.list_padding, right=self.list_padding
            ),
        )

        for msg in self.chat_history_data:
            if msg["sender"] == "user":
                self.chat_listview.controls.append(UserMessage(msg["content"]))
            elif msg["sender"] == "ai":
                self.chat_listview.controls.append(AiMessage(msg["content"]))

    # --- Input area ---
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

    # --- Input state ---
    def _on_input_change(self):
        has_text = bool(self.input_field.value and not self.input_field.value.isspace())
        self.send_icon.disabled = not has_text
        self.send_icon.opacity = 1.0 if has_text else 0.4
        self.send_icon.update()

    # --- Message handling ---
    def _handle_send(self):
        text = self.input_field.value
        if not text or text.isspace():
            return

        self.input_field.value = ""
        self.send_icon.disabled = True
        self.send_icon.opacity = 0.4
        self.input_field.update()
        self.send_icon.update()

        self._add_user_message(text)
        self._show_loading()

        text_copy = text

        async def _process():
            await asyncio.sleep(1.5)
            self._remove_loading()
            self._add_ai_message(
                f"This is a simulated response to: '{text_copy}'. Document processing logic will go here."
            )

        self.page_ref.run_task(_process)

    def _add_user_message(self, text: str):
        bubble = UserMessage(text)
        self.chat_listview.controls.append(bubble)
        self.chat_listview.update()

        is_first_message = len(self.chat_history_data) == 0
        self.chat_history_data.append({"sender": "user", "content": text})

        if self.is_logged_in:
            if self.chat_id is not None:
                insert_message(self.chat_id, "user", text)
                if is_first_message:
                    update_chat_title(self.chat_id, text[:75])
        else:
            self.page_ref.session.store.set(
                f"history_{self.chat_id}", self.chat_history_data
            )

    def _add_ai_message(self, text: str):
        bubble = AiMessage(text)
        self.chat_listview.controls.append(bubble)
        self.chat_listview.update()

        self.chat_history_data.append({"sender": "ai", "content": text})

        if self.is_logged_in:
            if self.chat_id is not None:
                insert_message(self.chat_id, "ai", text)
        else:
            self.page_ref.session.store.set(
                f"history_{self.chat_id}", self.chat_history_data
            )

    def _show_loading(self):
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

    # --- Responsive logic ---
    def _on_resize(self):
        width = self.page_ref.width

        if Responsive.crossed_breakpoint(width):
            config = Responsive.get_size()
            padding = config["list_padding"]
            self.appbar.update_margin(config["left_margin"])
            if self.chat_id is not None:
                self.chat_listview.padding = ft.Padding.only(
                    top=32, bottom=160, left=padding, right=padding
                )

            is_narrow = (width or 1200) < Breakpoint.MOBILE_BREAKPOINT
            self.drawer.visible = not is_narrow
            self.appbar.set_menu_visible(is_narrow)
            self.drawer.update()

        if self.upload_card is not None:
            self.upload_card.apply_responsive(width)
            self.upload_card.update()

        self.appbar.update()
        if self.chat_id is not None:
            self.chat_listview.update()
