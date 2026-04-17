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
            "gradient": ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=[
                    ft.Colors.with_opacity(0.0, ft.Colors.SURFACE),
                    ft.Colors.SURFACE,
                    ft.Colors.SURFACE,
                ],
                stops=[0.0, 0.4, 1.0],
            ),
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
    def input_field() -> dict:
        return {
            "hint_text": "Ask anything about the document...",
            "border": ft.InputBorder.NONE,
            "multiline": True,
            "min_lines": 1,
            "max_lines": 5,
            "cursor_height": 20,
            "expand": True,
            "text_align": ft.TextAlign.LEFT,
            "content_padding": ft.Padding.only(left=24, right=16, top=20, bottom=16),
            "shift_enter": True,
        }

    @staticmethod
    def send_button_icon() -> dict:
        return {
            "icon": ft.Icons.ARROW_UPWARD_ROUNDED,
            "icon_size": 18,
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

    @staticmethod
    def app_name() -> dict:
        return {
            "value": "Easy Docs AI",
            "style": ft.TextStyle(
                weight=ft.FontWeight.W_700,
                font_family=Config.FONT,
                size=20,
                color="#13DAEC",
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
