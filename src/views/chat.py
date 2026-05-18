import asyncio
import json
import uuid

import flet as ft
from flet.controls.services.shared_preferences import SharedPreferences

from components import Appbar, ChatDrawer, UploadCard
from components.chat import AiMessage, UserMessage
from components.utils import create_placeholder
from utils import (
    Config,
    Responsive,
    Style,
    get_chat_documents,
    get_messages,
    get_user,
    insert_message,
    update_chat_title,
)
from utils.ai.openrouter import chat_completion_stream
from utils.ai.rag import NO_DOCS_REPLY, build_guest_messages, build_rag_messages
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
        self.doc_text: str = ""

        self.is_streaming = False
        self.stop_event: asyncio.Event | None = None

        is_narrow = (page.width or 1200) < Breakpoint.MOBILE_BREAKPOINT
        self.is_narrow = is_narrow

        self.appbar: Appbar = Appbar(
            page=page,
            user_email=self.user_email,
            documents=self.uploaded_files,
            on_menu_click=self._toggle_drawer,
        )

        self.side_drawer = ChatDrawer(
            page,
            self.chat_id,
            self.is_logged_in,
            on_chat_deleted=self._on_chat_deleted,
        )
        self.side_drawer.visible = not is_narrow

        self.right_pane_container = ft.Container(
            content=self._build_right_pane(),
            expand=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            padding=ft.Padding.only(left=0 if is_narrow else Config.DRAWER_WIDTH),
        )

        self.side_drawer.left = 0
        self.side_drawer.top = 0
        self.side_drawer.bottom = 0

        self.controls = [
            ft.Stack(
                [
                    self.right_pane_container,
                    self.side_drawer,
                ],
                expand=True,
            ),
        ]

        self.appbar.set_menu_visible(is_narrow)
        page.on_resize = self._on_resize

        if self.chat_id is not None:
            page.run_task(self._setup_async)

    async def _setup_async(self):
        if not self.chat_id:
            return
        loaded = await self._load_chat_data(self.chat_id)
        if not loaded:
            await self._redirect_to_root()
            return
        self.appbar.set_documents(self.uploaded_files)
        self.chat_listview.controls = self._build_message_controls()
        self.chat_listview.update()

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

    async def _load_chat_data(self, chat_id: str) -> bool:
        if self.is_logged_in:
            try:
                doc_rows = await asyncio.to_thread(get_chat_documents, chat_id)
                self.uploaded_files = [d["file_name"] for d in doc_rows]
                db_messages = await asyncio.to_thread(get_messages, chat_id)
                self.chat_history_data = [
                    {"sender": m["sender"], "content": m["content"]}
                    for m in db_messages
                ]
            except Exception as err:
                print(f"Error fetching chat data: {err}")
                self.uploaded_files = []
                self.chat_history_data = []
        else:
            prefs = SharedPreferences()
            files_raw = await prefs.get(f"uploaded_files_{chat_id}")
            history_raw = await prefs.get(f"history_{chat_id}")
            self.uploaded_files = json.loads(files_raw) if files_raw else []
            self.chat_history_data = json.loads(history_raw) if history_raw else []
            self.doc_text = (await prefs.get(f"doc_text_{chat_id}")) or ""

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
        self.main_column = ft.Container(
            content=self.chat_listview,
            padding=ft.Padding.only(
                top=32, bottom=160, left=self.list_padding, right=self.list_padding
            ),
            expand=True,
            theme=Style.hidden_scrollbar_theme(),
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

    async def load_chat(self, route: str):
        new_chat_id = self._parse_chat_id(route)
        if new_chat_id is None and self._route_had_invalid_id(route):
            self.page_ref.run_task(self._redirect_to_root)
            return

        old_chat_id = self.chat_id
        self.route = route
        self.chat_id = new_chat_id
        self.uploaded_files = []
        self.chat_history_data = []
        self.doc_text = ""

        if new_chat_id is not None and not await self._load_chat_data(new_chat_id):
            self.page_ref.run_task(self._redirect_to_root)
            return

        self.appbar.set_documents(self.uploaded_files)
        await self.side_drawer.refresh_chats()
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

    async def _on_chat_deleted(self, deleted_chat_id: str):
        if deleted_chat_id == self.chat_id:
            await self.page_ref.push_route("/chat")

    # --- Drawer toggle (mobile hamburger) ---
    def _toggle_drawer(self, _e=None):
        self.side_drawer.visible = not self.side_drawer.visible
        self.side_drawer.update()

    # --- Chat history ---
    def _build_message_controls(self) -> list[ft.Control]:
        controls: list[ft.Control] = []
        for msg in self.chat_history_data:
            if msg["sender"] == "user":
                controls.append(UserMessage(msg["content"], is_narrow=self.is_narrow))
            elif msg["sender"] == "ai":
                controls.append(AiMessage(msg["content"], is_narrow=self.is_narrow))
        return controls

    def _build_chat_history(self):
        self.chat_listview = ft.ListView(
            **Style.chat_history(),
            controls=self._build_message_controls(),
        )

    # --- Input area ---
    def _build_input_area(self):
        self.send_icon = ft.IconButton(
            **Style.send_button_icon(self.is_narrow),
            on_click=self._handle_send,
            disabled=True,
            opacity=0.4,
        )

        self.input_field = ft.TextField(
            **Style.input_field(self.is_narrow),
            on_submit=self._handle_send,
            on_change=self._on_input_change,
        )

        btn_size = 32 if self.is_narrow else 40
        btn_wrap_right = 8 if self.is_narrow else 12
        btn_wrap_bottom = 4 if self.is_narrow else 6

        self.send_button = ft.Container(
            height=btn_size,
            width=btn_size,
            content=self.send_icon,
            offset=ft.Offset(0, -0.12) if self.is_narrow else None,
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
                        padding=ft.Padding.only(
                            right=btn_wrap_right, bottom=btn_wrap_bottom
                        ),
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
                    create_placeholder(self.is_narrow),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # --- Input state ---
    def _on_input_change(self):
        if self.is_streaming:
            return
        has_text = bool(self.input_field.value and not self.input_field.value.isspace())
        self.send_icon.disabled = not has_text
        self.send_icon.opacity = 1.0 if has_text else 0.4
        self.send_icon.update()

    def _set_streaming(self, streaming: bool):
        self.is_streaming = streaming
        if streaming:
            self.send_icon.icon = ft.Icons.STOP_ROUNDED
            self.send_icon.tooltip = "Stop"
            self.send_icon.disabled = False
            self.send_icon.opacity = 1.0
            self.send_icon.on_click = self._handle_stop
        else:
            self.send_icon.icon = ft.Icons.ARROW_UPWARD_ROUNDED
            self.send_icon.tooltip = None
            self.send_icon.on_click = self._handle_send
            has_text = bool(
                self.input_field.value and not self.input_field.value.isspace()
            )
            self.send_icon.disabled = not has_text
            self.send_icon.opacity = 1.0 if has_text else 0.4
        self.send_icon.update()

    def _handle_stop(self, _e=None):
        if self.stop_event is not None:
            self.stop_event.set()

    # --- Message handling ---
    def _handle_send(self, _e=None):
        if self.is_streaming:
            return

        text = self.input_field.value
        if not text or text.isspace():
            return

        self.input_field.value = ""
        self.input_field.update()

        text_copy = text
        chat_id_at_send = self.chat_id

        async def _process():
            self.stop_event = asyncio.Event()
            self._set_streaming(True)
            try:
                await self._add_user_message(text_copy)
                if not chat_id_at_send:
                    await self._add_ai_message(NO_DOCS_REPLY, chat_id_at_send)
                    return

                # messages: list[dict] | None = None
                try:
                    if self.is_logged_in:
                        messages, _ = await build_rag_messages(
                            chat_id_at_send, self.chat_history_data
                        )
                    else:
                        messages = build_guest_messages(
                            self.doc_text, self.chat_history_data
                        )
                except Exception as ex:
                    await self._add_ai_message(
                        f"Sorry — couldn't reach the model ({type(ex).__name__}).",
                        chat_id_at_send,
                    )
                    return

                if messages is None:
                    await self._add_ai_message(NO_DOCS_REPLY, chat_id_at_send)
                    return

                await self._stream_ai_message(chat_id_at_send, messages)
            finally:
                self._set_streaming(False)
                self.stop_event = None

        self.page_ref.run_task(_process)

    async def _stream_ai_message(
        self,
        chat_id: str,
        messages: list[dict],
    ):
        ai_bubble: AiMessage | None = None
        if chat_id == self.chat_id:
            ai_bubble = AiMessage("", is_narrow=self.is_narrow)
            if not ai_bubble:
                return
            self.chat_listview.controls.append(ai_bubble)
            self.page_ref.update()

        stop_event = self.stop_event
        full_text = ""
        try:
            async for chunk in chat_completion_stream(messages):
                if stop_event is not None and stop_event.is_set():
                    break
                full_text += chunk
                if ai_bubble is not None and chat_id == self.chat_id:
                    ai_bubble.set_text(full_text)
                    self.page_ref.update()
                elif ai_bubble is not None:
                    ai_bubble = None
        except Exception as ex:
            full_text = f"Sorry — couldn't reach the model ({type(ex).__name__})."
            if ai_bubble is not None and chat_id == self.chat_id:
                ai_bubble.set_text(full_text)
                self.page_ref.update()

        if not full_text:
            if ai_bubble is not None and chat_id == self.chat_id:
                try:
                    self.chat_listview.controls.remove(ai_bubble)
                    self.page_ref.update()
                except ValueError:
                    pass
            return

        self.chat_history_data.append({"sender": "ai", "content": full_text})

        if self.is_logged_in:
            await asyncio.to_thread(insert_message, chat_id, "ai", full_text)
        else:
            await SharedPreferences().set(
                f"history_{chat_id}", json.dumps(self.chat_history_data)
            )

    async def _add_user_message(self, text: str):
        bubble = UserMessage(text, is_narrow=self.is_narrow)
        self.chat_listview.controls.append(bubble)
        self.page_ref.update()

        is_first_message = len(self.chat_history_data) == 0
        self.chat_history_data.append({"sender": "user", "content": text})

        if self.is_logged_in:
            if self.chat_id is not None:
                await asyncio.to_thread(insert_message, self.chat_id, "user", text)
                if is_first_message:
                    await asyncio.to_thread(update_chat_title, self.chat_id, text[:75])
        else:
            await SharedPreferences().set(
                f"history_{self.chat_id}", json.dumps(self.chat_history_data)
            )

    async def _add_ai_message(
        self,
        text: str,
        chat_id: str | None,
    ):
        if chat_id != self.chat_id:
            if self.is_logged_in and chat_id is not None:
                await asyncio.to_thread(insert_message, chat_id, "ai", text)
            return

        bubble = AiMessage(text, is_narrow=self.is_narrow)
        self.chat_listview.controls.append(bubble)
        self.page_ref.update()

        self.chat_history_data.append({"sender": "ai", "content": text})

        if self.is_logged_in:
            if chat_id is not None:
                await asyncio.to_thread(insert_message, chat_id, "ai", text)
        else:
            await SharedPreferences().set(
                f"history_{chat_id}", json.dumps(self.chat_history_data)
            )

    # --- Responsive logic ---
    def _on_resize(self):
        width = self.page_ref.width
        if not width:
            return
        if Responsive.crossed_breakpoint(width):
            config = Responsive.get_size()
            padding = config["list_padding"]
            if self.chat_id is not None:
                self.main_column.padding = ft.Padding.only(
                    top=32, bottom=160, left=padding, right=padding
                )

            is_narrow = (width or 1200) < Breakpoint.MOBILE_BREAKPOINT
            self.is_narrow = is_narrow
            if self.chat_id is not None and hasattr(self, "chat_listview"):
                self.chat_listview.controls = self._build_message_controls()
                self.chat_listview.update()
            self.side_drawer.visible = not is_narrow
            self.right_pane_container.padding = ft.Padding.only(
                left=0 if is_narrow else Config.DRAWER_WIDTH
            )
            self.right_pane_container.update()
            self.appbar.set_menu_visible(is_narrow)
            self.side_drawer.update()

        self.appbar.update()
