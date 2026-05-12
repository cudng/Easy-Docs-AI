import flet as ft

from utils import Config, Responsive, Style, supabase


class ResetPassword(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        self.responsive = Responsive()

        # ── Form fields ─────────────────────────────────────────────
        self.password_field = ft.TextField(
            **Style.auth_field(),
            label="New Password",
            hint_text="Enter a new password",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=Config.PRIMARY),
            password=True,
            can_reveal_password=True,
            on_change=self._clear_error,
        )

        self.confirm_password_field = ft.TextField(
            **Style.auth_field(),
            label="Confirm Password",
            hint_text="Repeat the new password",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=Config.PRIMARY),
            password=True,
            can_reveal_password=True,
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
            "Update Password",
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
                        ft.Icon(
                            ft.Icons.LOCK_RESET_ROUNDED,
                            size=60,
                            color=Config.PRIMARY,
                        ),
                        ft.Text(
                            "Set New Password",
                            size=20,
                            weight=ft.FontWeight.W_700,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Enter and confirm your new password\nto regain access to your account",
                            size=14,
                            color=ft.Colors.OUTLINE,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        self.password_field,
                        self.confirm_password_field,
                        self.error_text,
                        self.success_text,
                        self.submit_btn,
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

    # ── Validation & submit ─────────────────────────────────────────
    def _on_submit(self, e=None):
        password = (self.password_field.value or "").strip()
        confirm = (self.confirm_password_field.value or "").strip()

        if not password:
            self._show_error("Please enter a new password")
            return
        if len(password) < 6:
            self._show_error("Password must be at least 6 characters")
            return
        if password != confirm:
            self._show_error("Passwords do not match")
            return

        try:
            response = supabase.auth.update_user({"password": password})
        except Exception as err:
            msg = str(err)
            if "Auth session missing" in msg or "session" in msg.lower():
                self._show_error(
                    "Recovery link expired or invalid. Please request a new reset link."
                )
            else:
                self._show_error(msg)
            return

        if not response.user:
            self._show_error("Couldn't update password. Please try again.")
            return

        self._show_success("Password updated. Redirecting to sign in…")
        self.page_ref.run_task(self._go_login)

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
    async def _go_login(self):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        await self.page_ref.push_route("/login")
