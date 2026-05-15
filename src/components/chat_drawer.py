import flet as ft

from utils import (
    Config,
    count_chat_documents,
    get_user,
    list_chats,
)

DRAWER_WIDTH = 280


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

        self.new_chat_btn = ft.Container(
            margin=ft.Margin.only(bottom=8),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=10,
            bgcolor=Config.PRIMARY,
            on_click=self._on_new_chat,
            ink=True,
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD, size=18, color=ft.Colors.BLACK),
                    ft.Text(
                        "New chat",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        font_family=Config.FONT,
                        color=ft.Colors.BLACK,
                    ),
                ],
                spacing=8,
                tight=True,
            ),
        )

        if self.is_logged_in:
            body = self._build_chat_list()
        else:
            body = self._build_guest_cta()

        super().__init__(
            width=DRAWER_WIDTH,
            padding=ft.Padding.symmetric(horizontal=12, vertical=16),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
            content=ft.Column(
                [
                    self.new_chat_btn,
                    body,
                ],
                spacing=0,
                expand=True,
            ),
        )

    # ── Logged-in: list of chats ────────────────────────────────────
    def _build_chat_list(self) -> ft.Control:
        user = get_user(self.page_ref)
        if user:
            user_id = user["user_id"]

            try:
                chats = list_chats(user_id)
            except Exception as err:
                print(f"Error fetching chats: {err}")
                chats = []

            items: list[ft.Control] = []
            for chat in chats:
                items.append(self._build_chat_row(chat))

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

            return ft.ListView(
                controls=items,
                expand=True,
                spacing=2,
            )
        return ft.ListView(
            controls=[
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
        )

    def _build_chat_row(self, chat: dict) -> ft.Control:
        chat_id = chat["id"]
        title = chat.get("title") or "Untitled"
        is_active = chat_id == self.current_chat_id

        try:
            doc_count = count_chat_documents(chat_id)
        except Exception as err:
            print(f"Error fetching chat documents: {err}")
            doc_count = 0

        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH if is_active else None,
            on_click=lambda _e, cid=chat_id: self.page_ref.run_task(
                self._go_to_chat, cid
            ),
            ink=True,
            content=ft.Row(
                [
                    ft.Text(
                        title,
                        size=13,
                        weight=ft.FontWeight.W_600
                        if is_active
                        else ft.FontWeight.W_400,
                        font_family=Config.FONT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        expand=True,
                    ),
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        border_radius=6,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.INSERT_DRIVE_FILE_OUTLINED,
                                    size=12,
                                    color=ft.Colors.OUTLINE,
                                ),
                                ft.Text(
                                    str(doc_count),
                                    size=11,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                            ],
                            spacing=3,
                            tight=True,
                        ),
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # ── Guest: sign-in CTA ──────────────────────────────────────────
    def _build_guest_cta(self) -> ft.Control:
        return ft.Container(
            margin=ft.Margin.only(top=8),
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.INFO_OUTLINE,
                                size=18,
                                color=ft.Colors.OUTLINE,
                            ),
                            ft.Text(
                                "Sign in to save chats",
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.ON_SURFACE,
                                font_family=Config.FONT,
                            ),
                        ],
                        spacing=6,
                        tight=True,
                    ),
                    ft.Text(
                        "Guest chats live only in this tab and disappear on refresh.",
                        size=12,
                        color=ft.Colors.OUTLINE,
                        font_family=Config.FONT,
                    ),
                    ft.TextButton(
                        "Sign in",
                        on_click=self._on_sign_in,
                        style=ft.ButtonStyle(
                            padding=ft.Padding.symmetric(horizontal=8, vertical=0),
                        ),
                    ),
                ],
                spacing=6,
                tight=True,
            ),
        )

    # ── Navigation handlers ─────────────────────────────────────────
    def _on_new_chat(self, _e=None):
        self.page_ref.run_task(self._go_new_chat)

    async def _go_new_chat(self):
        await self.page_ref.push_route("/chat")

    async def _go_to_chat(self, chat_id: str):
        await self.page_ref.push_route(f"/chat/{chat_id}")

    async def _on_sign_in(self, _e=None):
        await self.page_ref.push_route("/login")
