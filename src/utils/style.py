import flet as ft

from utils import Config


class Style:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    @staticmethod
    def input_container() -> dict:
        return {
            "padding": ft.Padding.only(left=16, right=16, top=24, bottom=24),
        }

    @staticmethod
    def input_row() -> dict:
        return {
            "bgcolor": ft.Colors.SURFACE,
            "border": ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            "border_radius": 30,
            "shadow": ft.BoxShadow(
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.SHADOW),
                offset=ft.Offset(0, 4),
            ),
        }

    @staticmethod
    def input_field(is_narrow: bool = False) -> dict:
        return {
            "hint_text": "Ask anything..." if is_narrow else "Ask anything about the document...",
            "hint_style": ft.TextStyle(
                size=13 if is_narrow else 14,
                color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
            ),
            "text_style": ft.TextStyle(size=13 if is_narrow else 14),
            "border": ft.InputBorder.NONE,
            "multiline": True,
            "min_lines": 1,
            "max_lines": 5,
            "cursor_height": 18 if is_narrow else 20,
            "expand": True,
            "text_align": ft.TextAlign.LEFT,
            "content_padding": (
                ft.Padding.only(left=16, right=8, top=14, bottom=12)
                if is_narrow
                else ft.Padding.only(left=24, right=16, top=20, bottom=16)
            ),
            "shift_enter": True,
        }

    @staticmethod
    def send_button_icon(is_narrow: bool = False) -> dict:
        return {
            "icon": ft.Icons.ARROW_UPWARD_ROUNDED,
            "icon_size": 14 if is_narrow else 18,
            "padding": ft.Padding.all(0),
            "bgcolor": Config.PRIMARY,
            "icon_color": ft.Colors.WHITE,
            "style": ft.ButtonStyle(
                shape=ft.CircleBorder(),
            ),
        }

    @staticmethod
    def settings_icon() -> dict:
        return {
            "icon": ft.Icons.TUNE_ROUNDED,
            "icon_size": 24,
            "icon_color": ft.Colors.OUTLINE,
            "tooltip": "Advanced Settings",
        }

    @staticmethod
    def chat_history() -> dict:
        return {
            "expand": True,
            "spacing": 24,
            "auto_scroll": True,
        }

    @staticmethod
    def hidden_scrollbar_theme() -> ft.Theme:
        return ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thumb_color=ft.Colors.TRANSPARENT,
                track_color=ft.Colors.TRANSPARENT,
                thickness=0,
            ),
        )

    @staticmethod
    def resources_visibility_toggle() -> dict:
        return {
            "content": "Show Sources",
            "height": 40,
            "icon": ft.Icons.VISIBILITY,
            "color": ft.Colors.WHITE,
            "bgcolor": Config.PRIMARY,
            "style": ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            "margin": ft.Margin.only(right=10),
        }

    # ── Appbar  ──────────────────────────────────────────────
    @staticmethod
    def appbar(actions: list[ft.Control]) -> dict:
        return {
            "leading_width": 275,
            "toolbar_height": 60,
            "center_title": True,
            "bgcolor": ft.Colors.SURFACE_CONTAINER_LOWEST,
            "actions": actions,
        }

    @staticmethod
    def app_name(is_narrow: bool = False) -> dict:
        return {
            "value": "Easy Docs AI",
            "style": ft.TextStyle(
                weight=ft.FontWeight.W_700,
                font_family=Config.FONT,
                size=14 if is_narrow else 20,
                color="#13DAEC",  # noqa
            ),
        }

    @staticmethod
    def app_logo() -> dict:
        return {
            "content": ft.Image(Config.SVG, color="#13DAEC"),  # noqa
            "padding": ft.Padding.only(top=10, bottom=10),
            "margin": ft.Margin.only(left=20),
        }

    @staticmethod
    def menu_button(items: list[ft.PopupMenuItem]) -> dict:
        return {
            "margin": ft.Margin.only(right=20),
            "content": ft.PopupMenuButton(
                icon=ft.Icons.MENU,
                tooltip="Menu",
                items=items,
                icon_color=Config.PRIMARY,
            ),
        }

    @staticmethod
    def auth_field() -> dict:
        return {
            "border_radius": 12,
            "border_color": ft.Colors.with_opacity(0.15, Config.PRIMARY),
            "focused_border_color": Config.PRIMARY,
            "focused_border_width": 2,
            "cursor_color": Config.PRIMARY,
            "content_padding": ft.Padding.symmetric(horizontal=16, vertical=18),
            "text_style": ft.TextStyle(
                font_family=Config.FONT,
                size=15,
            ),
            "label_style": ft.TextStyle(
                font_family=Config.FONT,
                size=14,
                color=ft.Colors.OUTLINE,
            ),
            "hint_style": ft.TextStyle(
                font_family=Config.FONT,
                size=14,
                color=ft.Colors.with_opacity(0.4, ft.Colors.ON_SURFACE),
            ),
        }

    @staticmethod
    def google_button() -> dict:
        return {
            "color": ft.Colors.ON_SURFACE,
            "bgcolor": ft.Colors.SURFACE,
            "style": ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                side=ft.BorderSide(1, ft.Colors.with_opacity(0.15, Config.PRIMARY)),
                overlay_color=ft.Colors.with_opacity(0.06, Config.PRIMARY),
                # padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            ),
            "height": 48,
            "width": 300,
            "content": ft.Row(
                [
                    ft.Image(
                        src="icons/google.svg",
                        width=20,
                        height=20,
                    ),
                    ft.Text(
                        "Sign up with Google",
                        size=15,
                        weight=ft.FontWeight.W_500,
                        font_family=Config.FONT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
            ),
        }

    @staticmethod
    def login_button() -> dict:
        return {
            "content": "Login",
            "bgcolor": Config.PRIMARY,
            "color": ft.Colors.WHITE,
            "margin": ft.Margin.only(right=40),
            "style": ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            "height": 40,
        }

    @staticmethod
    def sign_in_button() -> dict:
        return {
            "content": "Sign In",
            "style": ft.ButtonStyle(
                color=Config.PRIMARY,
                text_style=ft.TextStyle(
                    weight=ft.FontWeight.W_600,
                    font_family=Config.FONT,
                ),
            ),
        }

    @staticmethod
    def have_account() -> dict:
        return {
            "value": "Already have an account?",
            "size": 14,
            "color": ft.Colors.OUTLINE,
            "font_family": Config.FONT,
        }

    @staticmethod
    def create_account_label() -> dict:
        return {
            "value": "Create Account",
            "size": 24,
            "weight": ft.FontWeight.W_700,
            "font_family": Config.FONT,
            "text_align": ft.TextAlign.CENTER,
        }

    @staticmethod
    def sign_up_label() -> dict:
        return {
            "value": "Sign up to get started with Easy Docs AI",
            "size": 14,
            "color": ft.Colors.OUTLINE,
            "font_family": Config.FONT,
            "text_align": ft.TextAlign.CENTER,
        }

    @staticmethod
    def error_text() -> dict:
        return {
            "value": "",
            "color": Config.ERROR,
            "size": 13,
            "font_family": Config.FONT,
            "visible": False,
        }

    @staticmethod
    def register_button() -> dict:
        return {
            "content": "Create Account",
            "bgcolor": Config.PRIMARY,
            "color": ft.Colors.WHITE,
            "style": ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            "width": 300,
            "height": 48,
        }

    @staticmethod
    def new_chat_button(is_active: bool) -> dict:
        return {
            "content": "New chat",
            "height": 35,
            "expand": True,
            "icon": ft.Icons.ADD,
            "icon_color": ft.Colors.WHITE,
            "style": ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=Config.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            ),
            "visible": is_active,
        }

    # ── Document items ──────────────────────────────────────────────
    @staticmethod
    def doc_icon() -> dict:
        return {
            "icon": ft.Icons.INSERT_DRIVE_FILE_OUTLINED,
            "size": 18,
            "color": ft.Colors.OUTLINE,
        }

    @staticmethod
    def doc_title(name: str) -> dict:
        return {
            "value": name,
            "tooltip": name,
            "size": 13,
            "font_family": Config.FONT,
            "max_lines": 1,
            "overflow": ft.TextOverflow.ELLIPSIS,
            "expand": True,
        }

    @staticmethod
    def doc_container() -> dict:
        return {
            "width": Config.DOC_ITEM_WIDTH,
            "padding": ft.Padding.symmetric(horizontal=12, vertical=6),
        }

    @staticmethod
    def documents_menu(documents: list[ft.PopupMenuItem], length: int) -> dict:
        return {
            "margin": ft.Margin.only(right=4),
            "content": ft.PopupMenuButton(
                content=ft.Container(
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=8,
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.FOLDER_OPEN,
                                size=18,
                                color=Config.PRIMARY,
                            ),
                            ft.Text(
                                f"Documents ({length})",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                font_family=Config.FONT,
                            ),
                        ],
                        spacing=8,
                        tight=True,
                    ),
                ),
                tooltip="Selected documents",
                items=documents,
            ),
        }

    # ── Menu items ──────────────────────────────────────────────────
    @staticmethod
    def menu_item(email: str) -> dict:
        return {
            "padding": ft.Padding.symmetric(horizontal=12, vertical=6),
            "content": ft.Column(
                [
                    ft.Text(
                        "Signed in as",
                        size=11,
                        color=ft.Colors.OUTLINE,
                        font_family=Config.FONT,
                    ),
                    ft.Text(
                        email,
                        size=13,
                        color=Config.TEAL,
                        weight=ft.FontWeight.W_600,
                        font_family=Config.FONT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                spacing=2,
                tight=True,
            ),
        }

    @staticmethod
    def menu_icon(show: bool) -> dict:
        return {
            "icon": ft.Icons.VIEW_SIDEBAR_OUTLINED,
            "tooltip": "Toggle chats",
            "icon_color": Config.PRIMARY,
            "visible": show,
        }

    # ── Chat items ──────────────────────────────────────────────────
    @staticmethod
    def chat_row_title(title: str, is_active: bool) -> dict:
        return {
            "value": title,
            "size": 13,
            "weight": ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
            "font_family": Config.FONT,
            "max_lines": 1,
            "overflow": ft.TextOverflow.ELLIPSIS,
            "expand": True,
        }

    @staticmethod
    def guest_cta_style() -> dict:
        return {
            "margin": ft.Margin.only(top=8),
            "padding": ft.Padding.symmetric(horizontal=14, vertical=12),
            "border_radius": 10,
            "bgcolor": ft.Colors.SURFACE_CONTAINER_HIGH,
            "content": ft.Column(
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
                    ft.ResponsiveRow(
                        [
                            ft.Text(
                                "Guest chats live only in your browser and are not saved.",
                                size=12,
                                color=ft.Colors.OUTLINE,
                                font_family=Config.FONT,
                            ),
                        ]
                    ),
                ],
                spacing=6,
                tight=True,
            ),
        }

    @staticmethod
    def input_container_style(input_container: ft.Control) -> dict:
        return {
            "content": input_container,
            "alignment": ft.Alignment.BOTTOM_CENTER,
            "bottom": 0,
            "left": 0,
            "right": 0,
        }

    # ── Upload card ──────────────────────────────────────────────────
    @staticmethod
    def drop_title_style(is_logged_in: bool) -> dict:
        return {
            "value": "Upload your documents" if is_logged_in else "Upload a document",
            "size": 22,
            "weight": ft.FontWeight.W_600,
            "font_family": Config.FONT,
            "text_align": ft.TextAlign.CENTER,
        }

    @staticmethod
    def subtitle_top_style(is_logged_in: bool) -> dict:
        return {
            "value": (
                "Add up to 3 documents to chat with in this session"
                if is_logged_in
                else "Guest mode: 1 document, 1 chat, no history"
            ),
            "size": 14,
            "color": ft.Colors.OUTLINE,
            "font_family": Config.FONT,
            "text_align": ft.TextAlign.CENTER,
        }

    @staticmethod
    def pick_btn_style() -> dict:
        return {
            "content": "Pick a File",
            "icon": ft.Icons.FOLDER_OPEN,
            "bgcolor": Config.PRIMARY,
            "color": ft.Colors.BLACK,
            "style": ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=12),
            ),
        }

    @staticmethod
    def subtitle_style() -> dict:
        return {
            "value": "Supported formats: PDF, DOCX, TXT",
            "size": 13,
            "color": ft.Colors.OUTLINE,
            "font_family": Config.FONT,
            "text_align": ft.TextAlign.CENTER,
        }
