import flet as ft

from utils import Config, Responsive, Style, app_redirect_url, save_session, supabase


class LoginPage(ft.View):
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
            on_change=self._clear_error,
        )

        self.password_field = ft.TextField(
            **Style.auth_field(),
            label="Password",
            hint_text="Enter your password",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=Config.PRIMARY),
            password=True,
            can_reveal_password=True,
            on_submit=self._on_login,
            on_change=self._clear_error,
        )

        self.forgot_password = ft.Text(
            spans=[
                ft.TextSpan(
                    text="Forgot Password?",
                    style=ft.TextStyle(
                        size=13,
                        color=Config.PRIMARY,
                        font_family=Config.FONT,
                        weight=ft.FontWeight.W_500,
                    ),
                    on_click=self._go_forgot_password,
                ),
            ],
        )

        self.error_text = ft.Text(
            value="",
            color=Config.ERROR,
            size=13,
            font_family=Config.FONT,
            visible=False,
        )

        self.login_btn = ft.Button(
            "Sign In",
            bgcolor=Config.PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=300,
            height=48,
            on_click=self._on_login,
        )

        self.google_btn = ft.Button(
            **Style.google_button(),
            on_click=self._on_google_login,
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
                padding=ft.Padding.only(left=40, right=40, top=20, bottom=20),
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
                            ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                            size=60,
                            color=Config.PRIMARY,
                        ),
                        ft.Text(
                            "Welcome Back",
                            size=20,
                            weight=ft.FontWeight.W_700,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Sign in to continue to Easy Docs AI",
                            size=14,
                            color=ft.Colors.OUTLINE,
                            font_family=Config.FONT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        self.email_field,
                        self.password_field,
                        ft.Row(
                            [self.forgot_password],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        self.error_text,
                        self.login_btn,
                        self.or_divider,
                        self.google_btn,
                        ft.Row(
                            [
                                ft.Text(
                                    "Don't have an account?",
                                    size=14,
                                    color=ft.Colors.OUTLINE,
                                    font_family=Config.FONT,
                                ),
                                ft.TextButton(
                                    "Sign Up",
                                    style=ft.ButtonStyle(
                                        color=Config.PRIMARY,
                                        text_style=ft.TextStyle(
                                            weight=ft.FontWeight.W_600,
                                            font_family=Config.FONT,
                                        ),
                                    ),
                                    on_click=self._go_register,
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

    # ── Validation & submit ─────────────────────────────────────────
    def _on_login(self):
        email = (self.email_field.value or "").strip()
        password = (self.password_field.value or "").strip()

        if not email:
            self._show_error("Please enter your email")
            return
        if not password:
            self._show_error("Please enter your password")
            return

        self.page_ref.run_task(self._sign_in, email, password)

    async def _sign_in(self, email: str, password: str):
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except Exception as err:
            msg = str(err)
            if "Email not confirmed" in msg:
                self._show_error("Please confirm your email before signing in.")
            elif "Invalid login credentials" in msg:
                self._show_error("Incorrect email or password.")
            else:
                self._show_error(msg)
            return

        if not response.session:
            self._show_error("Sign in failed. Please try again.")
            return

        await save_session(response)
        self.page_ref.session.store.set(
            "user",
            {"user_id": response.user.id, "email": response.user.email},
        )
        await self.page_ref.push_route("/")

    def _on_google_login(self):
        self.page_ref.run_task(self._google_oauth)

    async def _google_oauth(self):
        redirect_url = app_redirect_url(self.page_ref, "/auth/callback")

        try:
            response = supabase.auth.sign_in_with_oauth(
                {
                    "provider": "google",
                    "options": {"redirect_to": redirect_url},
                }
            )
        except Exception as err:
            self._show_error(str(err))
            return

        if not response.url:
            self._show_error("Couldn't start Google sign-in.")
            return

        await ft.UrlLauncher().launch_url(
            response.url, web_only_window_name="_self"
        )

    def _show_error(self, msg: str):
        self.error_text.value = msg
        self.error_text.visible = True
        self.error_text.update()

    def _clear_error(self):
        if self.error_text.visible:
            self.error_text.visible = False
            self.error_text.update()

    # ── Navigation ──────────────────────────────────────────────────
    def _on_go_home(self):
        self.page_ref.run_task(self._go_home)

    async def _go_home(self):
        await self.page_ref.push_route("/")

    async def _go_register(self):
        await self.page_ref.push_route("/register")

    async def _go_forgot_password(self):
        await self.page_ref.push_route("/forgot-password")
