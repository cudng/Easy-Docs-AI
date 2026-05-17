import asyncio
import hashlib
import json
import uuid
from typing import Awaitable, Callable

import flet as ft
from flet.controls.services.shared_preferences import SharedPreferences

from utils import (
    Config,
    Style,
    count_document_chunks,
    count_user_chats,
    create_chat,
    delete_storage_object,
    get_document_by_hash,
    get_user,
    insert_chunks,
    insert_document,
    link_chat_document,
    upload_document_to_storage,
)
from utils.ai.chunk import chunk_text
from utils.ai.extract import extract_text
from utils.ai.openrouter import embed_texts


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

        self.drop_title = ft.Text(**Style.drop_title_style(self.is_logged_in))

        self.subtitle_top = ft.Text(**Style.subtitle_top_style(self.is_logged_in))

        self.pick_btn = ft.Button(
            **Style.pick_btn_style(),
            on_click=self._on_pick_click,
        )

        self.subtitle = ft.Text(**Style.subtitle_style())

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

        self.upload_zone_card = ft.Card(
            content=self.inner_column,
            elevation=10,
            height=400,
            width=500,
        )

        self.status_text = ft.Text(
            "Processing…",
            size=15,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.ON_SURFACE,
            text_align=ft.TextAlign.CENTER,
            font_family=Config.FONT,
        )
        self.status_filename = ft.Text(
            "",
            size=12,
            color=ft.Colors.OUTLINE,
            text_align=ft.TextAlign.CENTER,
            font_family=Config.FONT,
        )
        self.loading_card = ft.Card(
            elevation=10,
            height=400,
            width=500,
            content=ft.Column(
                [
                    ft.ProgressRing(
                        width=48,
                        height=48,
                        stroke_width=4,
                        color=Config.PRIMARY,
                    ),
                    ft.Container(height=8),
                    self.status_text,
                    self.status_filename,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
        )

        self.card_wrapper = ft.Container(
            content=self.upload_zone_card,
            on_click=self._on_pick_click,
            on_hover=self._on_zone_hover,
        )

        super().__init__(
            content=self.card_wrapper,
            alignment=ft.Alignment.CENTER,
        )

    # ── Sign-in link handler ────────────────────────────────────────
    async def _on_sign_in_click(self):
        await self.page_ref.push_route("/login")

    # ── Hover effect on card area ───────────────────────────────────
    def _on_zone_hover(self, e):
        is_hovered = e.data
        self.upload_zone_card.bgcolor = (
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

        oversize = [f.name for f in result if f.size > Config.MAX_FILE_SIZE_BYTES]
        if oversize:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        f"File too large (max 5 MB): {', '.join(oversize)}"
                    ),
                )
            )
            return

        self._set_processing(True)
        try:
            await self._process_upload(result)
        finally:
            self._set_processing(False)

    def _set_processing(self, processing: bool):
        self.pick_btn.disabled = processing
        self.pick_btn.text = "Processing…" if processing else "Choose file"
        if processing:
            self.card_wrapper.content = self.loading_card
            self.card_wrapper.on_click = None
            self.card_wrapper.on_hover = None
        else:
            self.card_wrapper.content = self.upload_zone_card
            self.card_wrapper.on_click = self._on_pick_click
            self.card_wrapper.on_hover = self._on_zone_hover
        self.card_wrapper.update()

    def _set_status(self, message: str, filename: str = ""):
        self.status_text.value = message
        self.status_filename.value = filename
        self.status_text.update()
        self.status_filename.update()

    async def _process_upload(self, result: list[ft.FilePickerFile]):
        user = get_user(self.page_ref)
        prefs = SharedPreferences()

        if user is None:
            # Guest: extract text, persist in browser localStorage
            chat_id = str(uuid.uuid4())
            f = result[0]
            self._set_status("Reading file…", f.name)
            try:
                text = await asyncio.to_thread(extract_text, f.name, f.bytes)
            except Exception as ex:
                self.page_ref.show_dialog(
                    ft.SnackBar(
                        content=ft.Text(f"Couldn't read {f.name}: {type(ex).__name__}"),
                    )
                )
                return
            self._set_status("Creating chat…", f.name)
            await prefs.set(f"uploaded_files_{chat_id}", json.dumps([f.name]))
            await prefs.set(f"doc_text_{chat_id}", text)
            await self.on_chat_created(chat_id)
            return

        user_id = user["user_id"]

        if count_user_chats(user_id) >= Config.MAX_CHATS_PER_USER:
            self.page_ref.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        f"Chat limit reached ({Config.MAX_CHATS_PER_USER}). Delete a chat to create a new one."
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
                    if count_document_chunks(existing["id"]) == 0:
                        self._set_status("Reading file…", f.name)
                        try:
                            text = await asyncio.to_thread(
                                extract_text, f.name, f.bytes
                            )
                        except Exception as ex:
                            self.page_ref.show_dialog(
                                ft.SnackBar(
                                    content=ft.Text(
                                        f"Couldn't read {f.name}: {type(ex).__name__}"
                                    ),
                                )
                            )
                            return
                        self._set_status("Splitting into chunks…", f.name)
                        chunks = chunk_text(text)
                        if chunks:
                            self._set_status("Generating embeddings…", f.name)
                            embeddings = await embed_texts(chunks)
                            self._set_status("Saving chunks…", f.name)
                            await asyncio.to_thread(
                                insert_chunks, existing["id"], chunks, embeddings
                            )
                    document_ids.append(existing["id"])
                    continue

                self._set_status("Reading file…", f.name)
                try:
                    text = await asyncio.to_thread(extract_text, f.name, f.bytes)
                except Exception as ex:
                    self.page_ref.show_dialog(
                        ft.SnackBar(
                            content=ft.Text(f"Couldn't read {f.name}: {type(ex).__name__}"),
                        )
                    )
                    return

                self._set_status("Splitting into chunks…", f.name)
                chunks = chunk_text(text)
                if not chunks:
                    self.page_ref.show_dialog(
                        ft.SnackBar(
                            content=ft.Text(f"{f.name} appears to be empty."),
                        )
                    )
                    return

                self._set_status("Generating embeddings…", f.name)
                embeddings = await embed_texts(chunks)

                self._set_status("Uploading document…", f.name)
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
                except Exception:
                    delete_storage_object(storage_path)
                    raise

                self._set_status("Saving chunks…", f.name)
                try:
                    await asyncio.to_thread(
                        insert_chunks, doc["id"], chunks, embeddings
                    )
                except Exception:
                    delete_storage_object(storage_path)
                    raise

                document_ids.append(doc["id"])

            self._set_status("Creating chat…")
            base_name = result[0].name.rsplit(".", 1)[0]
            title = base_name[:50] + "..." if len(base_name) > 50 else base_name
            chat = create_chat(user_id, title=title)
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
