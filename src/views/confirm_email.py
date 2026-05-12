from urllib.parse import parse_qs, urlparse

import flet as ft

from utils import Config, Style, supabase


class ConfirmEmailPage(ft.View):
    RESEND_COOLDOWN_SECONDS = 60

    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        self.email = self._extract_email(page.route)
        self._cooldown_remaining = 60

        # ── Feedback text ────────────────────────────────────────────
        self.feedback_text = ft.Text(
            value="",
            size=13,
            font_family=Config.FONT,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

        # ── Resend button ────────────────────────────────────────────
        self.resend_btn = ft.Button(
            content="Resend email",
            bgcolor=Config.PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            height=42,
            on_click=self._on_resend,
        )

        # ── Card layout ──────────────────────────────────────────────
        self.form_card = ft.Card(
            elevation=8,
            content=ft.Container(
                width=400,
                padding=ft.Padding.all(20),
                border_radius=16,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Home",
                                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                                    style=ft.ButtonStyle(
                                        color=Config.PRIMARY,
                                        text_style=ft.TextStyle(
                                            font_family=Config.FONT,
                                        ),
                                    ),
                                    on_click=self._on_go_home,
                                ),
                            ],
                        ),
                        ft.Icon(
                            ft.Icons.MARK_EMAIL_READ_ROUNDED,
                            size=60,
                            color=Config.PRIMARY,
                        ),
                        ft.Text(
                            "Check your email",
                            size=24,
                            weight=ft.FontWeight.W_700,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    "We sent a confirmation link to ",
                                ),
                                ft.TextSpan(
                                    self.email or "your email",
                                    style=ft.TextStyle(
                                        weight=ft.FontWeight.W_600,
                                        color=Config.PRIMARY,
                                        font_family=Config.FONT,
                                    ),
                                ),
                                ft.TextSpan(
                                    ". Click it to activate your account.",
                                ),
                            ],
                            size=14,
                            color=ft.Colors.OUTLINE,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "You can close this page — confirmation works on any device.",
                            size=12,
                            color=ft.Colors.OUTLINE,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        self.feedback_text,
                        self.resend_btn,
                        ft.Row(
                            [
                                ft.Text(
                                    "Already confirmed?",
                                    size=14,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                                ft.TextButton(
                                    **Style.sign_in_button(),
                                    on_click=self._go_login,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=14,
                ),
            ),
        )

        self.controls = [
            ft.Container(
                content=self.form_card,
                expand=True,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(horizontal=20),
            ),
        ]

    # ── Helpers ─────────────────────────────────────────────────────
    @staticmethod
    def _extract_email(route: str) -> str | None:
        parsed = urlparse(route)
        params = parse_qs(parsed.query)
        values = params.get("email")
        return values[0] if values else None

    def _build_redirect_url(self) -> str:
        base = (self.page_ref.url or "").rstrip("/")
        return f"{base}/auth/callback"

    def _show_feedback(self, msg: str, is_error: bool = False):
        self.feedback_text.value = msg
        self.feedback_text.color = Config.ERROR if is_error else Config.PRIMARY
        self.feedback_text.visible = True
        self.feedback_text.update()

    # ── Resend ──────────────────────────────────────────────────────
    def _on_resend(self):
        if self._cooldown_remaining > 0:
            return
        if not self.email:
            self._show_feedback(
                "Email address missing — please sign up again.", is_error=True
            )
            return

        try:
            supabase.auth.resend(
                {
                    "type": "signup",
                    "email": self.email,
                    "options": {"email_redirect_to": self._build_redirect_url()},
                }
            )
            self._show_feedback("Confirmation email resent.")
            self.page_ref.run_task(self._start_cooldown)
        except Exception as err:
            self._show_feedback(f"Could not resend: {err}", is_error=True)

    async def _start_cooldown(self):
        import asyncio

        self._cooldown_remaining = self.RESEND_COOLDOWN_SECONDS
        self.resend_btn.disabled = True
        while self._cooldown_remaining > 0:
            self.resend_btn.content = f"Resend email ({self._cooldown_remaining}s)"
            self.resend_btn.update()
            await asyncio.sleep(1)
            self._cooldown_remaining -= 1
        self.resend_btn.content = "Resend email"
        self.resend_btn.disabled = False
        self.resend_btn.update()

    # ── Navigation ──────────────────────────────────────────────────
    def _on_go_home(self):
        self.page_ref.run_task(self._go_home)

    async def _go_home(self):
        await self.page_ref.push_route("/")

    async def _go_login(self):
        await self.page_ref.push_route("/login")
