import flet as ft

from utils import Config, Responsive, Style


class RestorePassword(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        self.responsive = Responsive()

        # ── Form fields ─────────────────────────────────────────────
        self.email_field = ft.TextField(
            **Style.auth_field(),
            label="Email",
            hint_text="you@example.com",
            prefix_icon=ft.Icon(ft.Icons.EMAIL_OUTLINED, color=Config.PRIMARY),
            keyboard_type=ft.KeyboardType.EMAIL,
            on_submit=self._on_submit,
            on_change=self._clear_error,
        )

        self.error_text = ft.Text(
            value="",
            color=Config.ERROR,
            size=13,
            font_family=Config.FONT,
            visible=False,
        )

        self.success_text = ft.Text(
            value="",
            color=Config.TEAL,
            size=13,
            font_family=Config.FONT,
            visible=False,
        )

        self.submit_btn = ft.Button(
            "Send Reset Link",
            bgcolor=Config.PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=300,
            height=48,
            on_click=self._on_submit,
        )

        # ── Card layout ────────────────────────────────────────────
        self.form_card = ft.Card(
            elevation=8,
            content=ft.Container(
                width=400,
                padding=ft.Padding.only(left=40, right=40, top=20, bottom=20),
                border_radius=16,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Back to Sign In",
                                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                                    style=ft.ButtonStyle(
                                        color=Config.PRIMARY,
                                        text_style=ft.TextStyle(
                                            font_family=Config.FONT,
                                        ),
                                    ),
                                    on_click=self._go_login,
                                ),
                            ],
                        ),
                        ft.Icon(
                            ft.Icons.LOCK_RESET_ROUNDED,
                            size=60,
                            color=Config.PRIMARY,
                        ),
                        ft.Text(
                            "Reset Password",
                            size=20,
                            weight=ft.FontWeight.W_700,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Enter your email and we'll send you\na link to reset your password",
                            size=14,
                            color=ft.Colors.OUTLINE,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        self.email_field,
                        self.error_text,
                        self.success_text,
                        self.submit_btn,
                        ft.Row(
                            [
                                ft.Text(
                                    "Remember your password?",
                                    size=14,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                                ft.TextButton(
                                    "Sign In",
                                    style=ft.ButtonStyle(
                                        color=Config.PRIMARY,
                                        text_style=ft.TextStyle(
                                            weight=ft.FontWeight.W_600,
                                            font_family=Config.FONT,
                                        ),
                                    ),
                                    on_click=self._go_login,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
            ),
        )

        # ── Page layout ────────────────────────────────────────────
        self.controls = [
            ft.Container(
                content=self.form_card,
                expand=True,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(horizontal=20, vertical=40),
            ),
        ]

        page.on_resize = self._on_resize

    # ── Validation & submit ─────────────────────────────────────────
    def _on_submit(self, e=None):
        email = (self.email_field.value or "").strip()

        if not email:
            self._show_error("Please enter your email")
            return

        self._show_success("Password reset link has been sent to your email")

    def _show_error(self, msg: str):
        self.success_text.visible = False
        self.error_text.value = msg
        self.error_text.visible = True
        self.error_text.update()
        self.success_text.update()

    def _show_success(self, msg: str):
        self.error_text.visible = False
        self.success_text.value = msg
        self.success_text.visible = True
        self.success_text.update()
        self.error_text.update()

    def _clear_error(self, e=None):
        if self.error_text.visible:
            self.error_text.visible = False
            self.error_text.update()

    # ── Navigation ──────────────────────────────────────────────────
    async def _go_login(self, e=None):
        await self.page_ref.push_route("/login")

    # ── Responsive ──────────────────────────────────────────────────
    def _on_resize(self, e=None):
        width = self.page_ref.width

        if width < 480:
            card_w = width * 0.92
            btn_w = card_w - 80
            self.form_card.content.width = card_w
            self.submit_btn.width = btn_w
        else:
            self.form_card.content.width = 400
            self.submit_btn.width = 400
