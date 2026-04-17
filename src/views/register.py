from urllib.parse import quote

import flet as ft

from utils import Config, Responsive, Style, supabase


class RegisterPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        self.responsive = Responsive()

        # ── Form fields ─────────────────────────────────────────────
        self.name_field = ft.TextField(
            **Style.auth_field(),
            label="Full Name",
            hint_text="John Doe",
            prefix_icon=ft.Icon(ft.Icons.PERSON_OUTLINE, color=Config.PRIMARY),
            on_change=self._clear_error,
        )

        self.email_field = ft.TextField(
            **Style.auth_field(),
            label="Email",
            hint_text="you@example.com",
            prefix_icon=ft.Icon(ft.Icons.EMAIL_OUTLINED, color=Config.PRIMARY),
            keyboard_type=ft.KeyboardType.EMAIL,
            on_change=self._clear_error,
        )

        self.password_field = ft.TextField(
            **Style.auth_field(),
            label="Password",
            hint_text="Create a password",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=Config.PRIMARY),
            password=True,
            can_reveal_password=True,
            on_change=self._clear_error,
        )

        self.confirm_password_field = ft.TextField(
            **Style.auth_field(),
            label="Confirm Password",
            hint_text="Repeat your password",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=Config.PRIMARY),
            password=True,
            can_reveal_password=True,
            on_submit=self._on_register,
            on_change=self._clear_error,
        )

        self.error_text = ft.Text(**Style.error_text())

        self.register_btn = ft.Button(
            **Style.register_button(),
            on_click=self._on_register,
        )

        self.google_btn = ft.Button(
            **Style.google_button(),
            on_click=self._on_google_register,
        )

        # ── Divider ────────────────────────────────────────────────
        self.or_divider = ft.Row(
            [
                ft.Container(
                    ft.Divider(color=ft.Colors.with_opacity(0.15, Config.PRIMARY)),
                    expand=True,
                ),
                ft.Text(
                    "or",
                    size=14,
                    color=ft.Colors.OUTLINE,
                    font_family=Config.FONT,
                ),
                ft.Container(
                    ft.Divider(color=ft.Colors.with_opacity(0.15, Config.PRIMARY)),
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )

        # ── Card layout ────────────────────────────────────────────
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
                            ft.Icons.PERSON_ADD_ROUNDED,
                            size=44,
                            color=Config.PRIMARY,
                        ),
                        ft.Text(
                            **Style.create_account_label(),
                        ),
                        ft.Text(**Style.sign_up_label()),
                        self.name_field,
                        self.email_field,
                        self.password_field,
                        self.confirm_password_field,
                        self.error_text,
                        self.register_btn,
                        self.or_divider,
                        self.google_btn,
                        ft.Row(
                            [
                                ft.Text(
                                    **Style.have_account(),
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
                padding=ft.Padding.symmetric(horizontal=20),
            ),
        ]

        # page.on_resize = self._on_resize

    # ── Validation & submit ─────────────────────────────────────────
    def _on_register(self, e=None):
        name = (self.name_field.value or "").strip()
        email = (self.email_field.value or "").strip()
        password = (self.password_field.value or "").strip()
        confirm = (self.confirm_password_field.value or "").strip()

        if not name:
            self._show_error("Please enter your name")
            return
        if not email:
            self._show_error("Please enter your email")
            return
        if not password:
            self._show_error("Please enter a password")
            return
        if len(password) < 6:
            self._show_error("Password must be at least 6 characters")
            return
        if password != confirm:
            self._show_error("Passwords do not match")
            return

        redirect_url = f"{(self.page_ref.url or '').rstrip('/')}/auth/callback"
        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "email_redirect_to": redirect_url,
                        "data": {"full_name": name},
                    },
                }
            )
        except Exception as err:
            self._show_error(str(err))
            return

        if response.user and not response.user.identities:
            self._show_error("This email is already registered.")
            return

        if response.session is None:
            self.page_ref.run_task(self._go_confirm_email, email)
        else:
            self.page_ref.run_task(self._go_home)

    def _on_google_register(self, e=None):
        self.page_ref.run_task(self._go_home)

    def _show_error(self, msg: str):
        self.error_text.value = msg
        self.error_text.visible = True
        self.error_text.update()

    def _clear_error(self, e=None):
        if self.error_text.visible:
            self.error_text.visible = False
            self.error_text.update()

    # ── Navigation ──────────────────────────────────────────────────
    def _on_go_home(self, e=None):
        self.page_ref.run_task(self._go_home)

    async def _go_home(self):
        await self.page_ref.push_route("/")

    async def _go_confirm_email(self, email: str):
        await self.page_ref.push_route(f"/confirm-email?email={quote(email)}")

    async def _go_login(self, e=None):
        await self.page_ref.push_route("/login")
