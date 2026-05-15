import hashlib
import uuid
from typing import Awaitable, Callable

import flet as ft

from utils import (
    Config,
    count_user_chats,
    create_chat,
    delete_storage_object,
    get_document_by_hash,
    get_user,
    insert_document,
    link_chat_document,
    upload_document_to_storage,
)

MAX_CHATS_PER_USER = 10
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # matches documents.size_bytes CHECK constraint


class UploadCard(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        on_chat_created: Callable[[str], Awaitable[None]],
    ):
        self.page_ref = page
        self.on_chat_created = on_chat_created

        user = get_user(page)
        self.is_logged_in = user is not None
        self.max_files = 3 if self.is_logged_in else 1

        self.upload_icon = ft.Icon(
            ft.Icons.CLOUD_UPLOAD_OUTLINED,
            size=64,
            color=Config.PRIMARY,
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        self.drop_title = ft.Text(
            "Upload your documents" if self.is_logged_in else "Upload a document",
            size=22,
            weight=ft.FontWeight.W_600,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.subtitle_top = ft.Text(
            (
                "Add up to 3 documents to chat with in this session"
                if self.is_logged_in
                else "Guest mode: 1 document, 1 chat, no history"
            ),
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

        self.guest_notice = ft.Container(
            visible=not self.is_logged_in,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            content=ft.Row(
                [
                    ft.Icon(
                        ft.Icons.INFO_OUTLINE,
                        size=18,
                        color=ft.Colors.OUTLINE,
                    ),
                    ft.Text(
                        "Sign in to chat with up to 3 documents and keep multiple chats.",
                        size=13,
                        color=ft.Colors.ON_SURFACE,
                        font_family=Config.FONT,
                    ),
                    ft.TextButton(
                        "Sign in",
                        on_click=self._on_sign_in_click,
                        style=ft.ButtonStyle(
                            padding=ft.Padding.symmetric(horizontal=8, vertical=0),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                wrap=True,
            ),
        )

        self.inner_column = ft.Column(
            [
                self.upload_icon,
                self.drop_title,
                self.subtitle_top,
                ft.Container(height=4),
                self.pick_btn,
                ft.Container(height=4),
                self.subtitle,
                self.guest_notice,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        self.upload_zone = ft.Container(
            padding=ft.Padding.symmetric(horizontal=40, vertical=60),
            content=self.inner_column,
            border_radius=12,
        )

        self.upload_zone_card = ft.Card(
            content=self.upload_zone,
            elevation=10,
        )

        self.card_wrapper = ft.Container(
            content=self.upload_zone_card,
            width=700,
            alignment=ft.Alignment.CENTER,
            border_radius=12,
            on_click=self._on_pick_click,
            on_hover=self._on_zone_hover,
            ink=True,
        )

        super().__init__(
            content=self.card_wrapper,
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.symmetric(horizontal=20, vertical=40),
        )

    # ── Sign-in link handler ────────────────────────────────────────
    async def _on_sign_in_click(self):
        await self.page_ref.push_route("/login")

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
            allow_multiple=self.is_logged_in,
            with_data=True,
        )

        if not result:
            return

        if len(result) > self.max_files:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        f"Only the first {self.max_files} files will be used."
                    ),
                )
            )
            result = result[: self.max_files]

        oversize = [f.name for f in result if f.size > MAX_FILE_SIZE_BYTES]
        if oversize:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        f"File too large (max 5 MB): {', '.join(oversize)}"
                    ),
                )
            )
            return

        user = get_user(self.page_ref)

        if user is None:
            # Guest: in-memory only
            chat_id = str(uuid.uuid4())
            selected_names = [f.name for f in result]
            self.page_ref.session.store.set(f"uploaded_files_{chat_id}", selected_names)
            await self.on_chat_created(chat_id)
            return

        # Logged-in: persist to Supabase
        user_id = user["user_id"]

        if count_user_chats(user_id) >= MAX_CHATS_PER_USER:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        f"Chat limit reached ({MAX_CHATS_PER_USER}). Delete a chat to create a new one."
                    ),
                )
            )
            return

        try:
            document_ids: list[str] = []
            for f in result:
                file_hash = hashlib.sha256(f.bytes).hexdigest()
                ext = f.name.rsplit(".", 1)[-1].lower()

                existing = get_document_by_hash(user_id, file_hash)
                if existing:
                    document_ids.append(existing["id"])
                    continue

                storage_path = upload_document_to_storage(
                    user_id, file_hash, ext, f.bytes
                )
                try:
                    doc = insert_document(
                        user_id=user_id,
                        file_name=f.name,
                        storage_path=storage_path,
                        size_bytes=f.size,
                        file_hash=file_hash,
                    )
                    document_ids.append(doc["id"])
                except Exception:
                    delete_storage_object(storage_path)
                    raise

            chat = create_chat(user_id, title=result[0].name[:75])
            chat_id = chat["id"]

            for doc_id in document_ids:
                link_chat_document(chat_id, doc_id)
        except Exception as ex:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(f"Upload failed: {type(ex).__name__}: {ex}"),
                )
            )
            return

        await self.on_chat_created(chat_id)

    # ── Responsive sizing (parent invokes on page resize) ───────────
    def apply_responsive(self, width: int | float | None):
        if width is None:
            return

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
