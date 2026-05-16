import flet as ft

from utils import (
    Config,
    Style,
    count_chat_documents,
    delete_chat,
    get_user,
    list_chats,
    update_chat_title,
)


class ChatDrawer(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        current_chat_id: str | None,
        is_logged_in: bool,
    ):
        self.page_ref = page
        self.current_chat_id = current_chat_id
        self.is_logged_in = is_logged_in

        self.new_chat_btn = ft.Button(
            **Style.new_chat_button(self.is_logged_in),
            on_click=self._on_new_chat,
        )

        if self.is_logged_in:
            self.body = self._build_chat_list()
        else:
            self.body = self._build_guest_cta()

        super().__init__(
            width=Config.DRAWER_WIDTH,
            padding=ft.Padding.symmetric(horizontal=12, vertical=16),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            border=ft.Border.only(right=ft.BorderSide(width=0.1)),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.new_chat_btn,
                        ],
                        margin=ft.Margin.only(bottom=10),
                    ),
                    ft.Divider(height=10),
                    ft.Row(
                        [
                            ft.Text(
                                "Chats",
                                size=16,
                                weight=ft.FontWeight.W_700,
                                margin=ft.Margin.only(top=10, bottom=10),
                            ),
                        ]
                    ),
                    self.body,
                ],
                spacing=0,
                expand=True,
            ),
        )

    # ── Logged-in: list of chats ────────────────────────────────────
    def _build_chat_list(self) -> ft.ListView:
        return ft.ListView(
            controls=self._build_chat_items(),
            expand=True,
            spacing=2,
        )

    def _build_chat_items(self) -> list[ft.Control]:
        self._row_refs: dict[str, dict] = {}
        user = get_user(self.page_ref)
        if not user:
            return [
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=8, vertical=12),
                    content=ft.Text(
                        "No chats yet. Pick a file to start one...",
                        size=12,
                        color=ft.Colors.OUTLINE,
                        font_family=Config.FONT,
                    ),
                )
            ]

        try:
            chats = list_chats(user["user_id"])
        except Exception as err:
            print(f"Error fetching chats: {err}")
            chats = []

        items: list[ft.Control] = [
            self._build_chat_row(chat, index) for index, chat in enumerate(chats)
        ]

        if not items:
            items.append(
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=8, vertical=12),
                    content=ft.Text(
                        "No chats yet. Pick a file to start one.",
                        size=12,
                        color=ft.Colors.OUTLINE,
                        font_family=Config.FONT,
                    ),
                )
            )
        return items

    def refresh_chats(self):
        if not self.is_logged_in:
            return
        self.body.controls = self._build_chat_items()
        self.body.update()

    def _build_chat_row(self, chat: dict, index: int) -> ft.Control:
        chat_id = chat["id"]
        title = chat.get("title") or "Untitled"
        is_active = chat_id == self.current_chat_id

        try:
            doc_count = count_chat_documents(chat_id)
        except Exception as err:
            print(f"Error fetching chat documents: {err}")
            doc_count = 0

        title_text = ft.Text(**Style.chat_row_title(title, is_active))
        container = ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=2),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH if is_active else None,
            tooltip=title,
            on_click=lambda _e, cid=chat_id: self.page_ref.run_task(
                self._go_to_chat, cid
            ),
            ink=True,
            content=ft.Row(
                [
                    title_text,
                    ft.TextField(
                        value=title,
                        visible=False,
                        border=ft.InputBorder.NONE,
                    ),
                    ft.PopupMenuButton(
                        key="popup",
                        menu_position=ft.PopupMenuPosition.UNDER,
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED),
                                        ft.Text(f"Documents: {doc_count}"),
                                    ],
                                ),
                            ),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.EDIT),
                                        ft.Text("Edit Title"),
                                    ]
                                ),
                                on_click=lambda _: self.update_chat_title(
                                    chat_id, index
                                ),
                            ),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.DELETE, color=ft.Colors.ERROR),
                                        ft.Text("Delete Chat"),
                                    ]
                                ),
                                on_click=lambda _: self._on_delete_chat(chat_id, index),
                            ),
                        ],
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        self._row_refs[chat_id] = {"container": container, "text": title_text}
        return container

    def set_active(self, chat_id: str | None):
        self.current_chat_id = chat_id
        if not hasattr(self, "_row_refs"):
            return
        for cid, refs in self._row_refs.items():
            is_active = cid == chat_id
            refs["container"].bgcolor = (  # noqa
                ft.Colors.SURFACE_CONTAINER_HIGH if is_active else None
            )
            refs["text"].weight = (  # noqa
                ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400
            )
        self.body.update()

    # ── Guest: sign-in CTA ──────────────────────────────────────────
    @staticmethod
    def _build_guest_cta() -> ft.Control:
        return ft.Container(**Style.guest_cta_style())

    # ── Navigation handlers ─────────────────────────────────────────
    def _on_new_chat(self, _e=None):
        self.page_ref.run_task(self._go_new_chat)

    def update_chat_title(self, chat_id: str, index: int):

        # container = self._row_refs[chat_id]["container"]
        chat_row = self.body.controls[index].content  # noqa
        text_control = chat_row.controls[0]
        text_field_control = chat_row.controls[1]

        def on_submit():
            new_title = text_field_control.value
            print(f"New title: {new_title}")
            if len(new_title) == 0:
                text_field_control.error_text = "Title cannot be empty"
                return
            try:
                self.page_ref.run_thread(update_chat_title, chat_id, new_title)
                text_field_control.visible = False
                text_control.value = new_title
                text_control.visible = True
                chat_row.update()
            except Exception as err:
                print(f"Error updating chat title: {err}")
                text_field_control.error_text = "Error updating title"
                return

        def cancel(_e):
            text_field_control.visible = False
            text_control.visible = True
            chat_row.update()

        text_field_control.visible = True
        text_control.visible = False
        text_field_control.autofocus = True
        text_field_control.on_submit = on_submit
        text_field_control.on_tap_outside = cancel
        chat_row.update()

    def _on_delete_chat(self, chat_id: str, index: int):
        try:
            self.page_ref.run_thread(delete_chat, chat_id)
            self.body.controls.pop(index)  # noqa
            self.body.update()
        except Exception as err:
            print(f"Error deleting chat: {err}")

    async def _go_new_chat(self):
        await self.page_ref.push_route("/chat")

    async def _go_to_chat(self, chat_id: str):
        await self.page_ref.push_route(f"/chat/{chat_id}")

    async def _on_sign_in(self):
        await self.page_ref.push_route("/login")
