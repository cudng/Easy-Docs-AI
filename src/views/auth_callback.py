from urllib.parse import parse_qs, urlparse

import flet as ft

from utils import Config, save_session, supabase


class AuthCallbackPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(padding=0, route=page.route)
        self.page_ref = page

        self.status_icon = ft.ProgressRing(
            color=Config.PRIMARY,
            width=40,
            height=40,
        )

        self.title_text = ft.Text(
            "Confirming your email…",
            size=20,
            weight=ft.FontWeight.W_700,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.subtitle_text = ft.Text(
            "Hang tight, this only takes a moment.",
            size=14,
            color=ft.Colors.OUTLINE,
            font_family=Config.FONT,
            text_align=ft.TextAlign.CENTER,
        )

        self.action_btn = ft.Button(
            content="Go to Sign In",
            bgcolor=Config.PRIMARY,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=260,
            height=44,
            visible=False,
            on_click=self._on_action,
        )

        self.form_card = ft.Card(
            elevation=8,
            content=ft.Container(
                width=400,
                padding=ft.Padding.all(28),
                border_radius=16,
                content=ft.Column(
                    [
                        self.status_icon,
                        self.title_text,
                        self.subtitle_text,
                        self.action_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
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

        self._action_route = "/login"
        self.page_ref.run_task(self._handle_callback)

    # ── Callback handling ──────────────────────────────────────────
    async def _handle_callback(self):
        params = self._parse_query(self.page_ref.route)

        error = params.get("error_description") or params.get("error")
        if error:
            self._show_error(error, action_label="Back to Sign Up", route="/register")
            return

        code = params.get("code")
        token_hash = params.get("token_hash")
        otp_type = params.get("type")
        access_token = params.get("access_token")
        refresh_token = params.get("refresh_token")
        next_route = params.get("next") or "/"
        is_recovery = otp_type == "recovery" or next_route == "/reset-password"

        try:
            if code:
                response = supabase.auth.exchange_code_for_session({"auth_code": code})
            elif access_token and refresh_token:
                response = supabase.auth.set_session(access_token, refresh_token)
            elif token_hash and otp_type:
                response = supabase.auth.verify_otp(
                    {"token_hash": token_hash, "type": otp_type}
                )
            else:
                self._show_error(
                    "Missing confirmation parameters in the link.",
                    action_label="Back to Sign Up",
                    route="/register",
                )
                return
        except Exception as err:
            if is_recovery:
                self._show_error(
                    f"We couldn't verify your reset link: {err}",
                    action_label="Request New Link",
                    route="/forgot-password",
                )
            else:
                self._show_error(
                    f"We couldn't confirm your email: {err}",
                    action_label="Back to Sign Up",
                    route="/register",
                )
            return

        if is_recovery:
            self._show_recovery_success()
            await self.page_ref.push_route("/reset-password")
            return

        if response.session:
            await save_session(response)
            self.page_ref.session.store.set(
                "user",
                {"user_id": response.user.id, "email": response.user.email},
            )

        self._show_success()
        await self.page_ref.push_route("/")

    # ── UI helpers ─────────────────────────────────────────────────
    def _show_success(self):
        self.status_icon.visible = False
        self.title_text.value = "Email confirmed!"
        self.subtitle_text.value = "Taking you to your dashboard…"
        self.form_card.update()

    def _show_recovery_success(self):
        self.status_icon.visible = False
        self.title_text.value = "Reset link verified"
        self.subtitle_text.value = "Taking you to set a new password…"
        self.form_card.update()

    def _show_error(self, msg: str, action_label: str, route: str):
        self.status_icon.visible = False
        self.title_text.value = "Confirmation failed"
        self.subtitle_text.value = msg
        self.subtitle_text.color = Config.ERROR
        self.action_btn.content = action_label
        self.action_btn.visible = True
        self._action_route = route
        self.form_card.update()

    # ── Navigation ─────────────────────────────────────────────────
    def _on_action(self):
        self.page_ref.run_task(self._go_to_action_route)

    async def _go_to_action_route(self):
        await self.page_ref.push_route(self._action_route)

    # ── Parsing ────────────────────────────────────────────────────
    @staticmethod
    def _parse_query(route: str) -> dict[str, str]:
        parsed = urlparse(route)
        flat = {k: v[0] for k, v in parse_qs(parsed.query).items() if v}
        if parsed.fragment:
            for k, v in parse_qs(parsed.fragment).items():
                if v and k not in flat:
                    flat[k] = v[0]
        return flat
