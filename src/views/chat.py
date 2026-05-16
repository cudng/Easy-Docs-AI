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
        self.user_email = user["email"] if user else None

        self.chat_id: str | None = self._parse_chat_id(page.route)
        if self.chat_id is None and self._route_had_invalid_id(page.route):
            self.controls = []
            page.run_task(self._redirect_to_root)
            return

        self.config = Responsive().get_size()
        self.left_margin = self.config["left_margin"]
        self.list_padding = self.config["list_padding"]

        self.uploaded_files: list[str] = []
        self.chat_history_data: list[dict] = []

        if self.chat_id is not None:
            if not self._load_chat_data(self.chat_id):
                self.controls = []
                page.run_task(self._redirect_to_root)
                return

        is_narrow = (page.width or 1200) < Breakpoint.MOBILE_BREAKPOINT

        self.appbar: Appbar = Appbar(
            page=page,
            user_email=self.user_email,
            documents=self.uploaded_files,
            on_menu_click=self._toggle_drawer,
        )

        self.side_drawer = ChatDrawer(page, self.chat_id, self.is_logged_in)
        self.side_drawer.visible = not is_narrow

        self.right_pane_container = ft.Container(
            content=self._build_right_pane(),
            expand=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        )

        self.controls = [
            ft.Row(
                [
                    self.side_drawer,
                    self.right_pane_container,
                ],
                expand=True,
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        ]

        self.appbar.set_menu_visible(is_narrow)
        page.on_resize = self._on_resize

    @staticmethod
    def _parse_chat_id(route: str) -> str | None:
        parts = route.split("/")
        raw = parts[2] if len(parts) > 2 and parts[2] else None
        if raw is None:
            return None
        try:
            return str(uuid.UUID(raw))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _route_had_invalid_id(route: str) -> bool:
        parts = route.split("/")
        raw = parts[2] if len(parts) > 2 and parts[2] else None
        if raw is None:
            return False
        try:
            uuid.UUID(raw)
            return False
        except (ValueError, TypeError):
            return True

    def _load_chat_data(self, chat_id: str) -> bool:
        if self.is_logged_in:
            try:
                doc_rows = get_chat_documents(chat_id)
                self.uploaded_files = [d["file_name"] for d in doc_rows]
                db_messages = get_messages(chat_id)
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
                self.page_ref.session.store.get(f"uploaded_files_{chat_id}") or []
            )
            self.chat_history_data = (
                self.page_ref.session.store.get(f"history_{chat_id}") or []
            )

        return (
            isinstance(self.uploaded_files, list)
            and bool(self.uploaded_files)
            and all(isinstance(x, str) for x in self.uploaded_files)
        )

    def _build_right_pane(self) -> ft.Control:
        if self.chat_id is None:
            self.upload_card = UploadCard(
                self.page_ref, on_chat_created=self._on_chat_created
            )
            return self.upload_card

        self.upload_card = None
        self._build_chat_history()
        self._build_input_area()
        self.main_column = ft.Column(
            controls=[self.chat_listview],
            expand=True,
            scroll=None,
        )
        return ft.Container(
            content=ft.Stack(
                [
                    self.main_column,
                    ft.Container(**Style.input_container_style(self.input_container)),
                ],
                expand=True,
            ),
            expand=True,
        )

    def load_chat(self, route: str):
        new_chat_id = self._parse_chat_id(route)
        if new_chat_id is None and self._route_had_invalid_id(route):
            self.page_ref.run_task(self._redirect_to_root)
            return

        old_chat_id = self.chat_id
        self.route = route
        self.chat_id = new_chat_id
        self.uploaded_files = []
        self.chat_history_data = []

        if new_chat_id is not None and not self._load_chat_data(new_chat_id):
            self.page_ref.run_task(self._redirect_to_root)
            return

        self.appbar.documents = self.uploaded_files
        self.side_drawer.refresh_chats()
        self.side_drawer.set_active(new_chat_id)

        if old_chat_id is not None and new_chat_id is not None:
            self.chat_listview.controls = self._build_message_controls()
            self.chat_listview.update()
            return

        self.right_pane_container.content = self._build_right_pane()
        self.right_pane_container.update()

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
        self.side_drawer.visible = not self.side_drawer.visible
        self.side_drawer.update()

    # --- Chat history ---
    def _build_message_controls(self) -> list[ft.Control]:
        controls: list[ft.Control] = []
        for msg in self.chat_history_data:
            if msg["sender"] == "user":
                controls.append(UserMessage(msg["content"]))
            elif msg["sender"] == "ai":
                controls.append(AiMessage(msg["content"]))
        return controls

    def _build_chat_history(self):
        self.chat_listview = ft.ListView(
            **Style.chat_history(),
            padding=ft.Padding.only(
                top=32, bottom=160, left=self.list_padding, right=self.list_padding
            ),
            controls=self._build_message_controls(),
        )

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
        if not width:
            return
        if Responsive.crossed_breakpoint(width):
            config = Responsive.get_size()
            padding = config["list_padding"]
            if self.chat_id is not None:
                self.chat_listview.padding = ft.Padding.only(
                    top=32, bottom=160, left=padding, right=padding
                )

            is_narrow = (width or 1200) < Breakpoint.MOBILE_BREAKPOINT
            self.side_drawer.visible = not is_narrow
            self.appbar.set_menu_visible(is_narrow)
            self.side_drawer.update()

        self.appbar.update()
