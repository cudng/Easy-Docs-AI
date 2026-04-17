import asyncio

import flet as ft

from views import (
    AuthCallbackPage,
    ChatPage,
    ConfirmEmailPage,
    HomePage,
    LoginPage,
    PageNotFound,
    RegisterPage,
    RestorePassword,
    SessionMode,
)


class RouteHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.db = db

    def route(self, e=None):
        """Called directly on the startup or passed to page.on_route_change."""
        self.page.views.clear()

        match self.page.route:
            case "/":
                self.page.views.append(HomePage(page=self.page))

            case "/session":
                self.page.views.append(SessionMode(page=self.page))

            case route if route.startswith("/session/chat"):
                self.page.views.append(ChatPage(page=self.page))

            case "/register":
                self.page.views.append(RegisterPage(self.page))

            case "/login":
                self.page.views.append(LoginPage(self.page))

            case "/forgot-password":
                self.page.views.append(RestorePassword(self.page))

            case route if route.startswith("/confirm-email"):
                self.page.views.append(ConfirmEmailPage(self.page))

            case route if route.startswith("/auth/callback"):
                self.page.views.append(AuthCallbackPage(self.page))

            # case "/settings":
            #     self.page.views.append(views.Settings(self.page))

            case _:
                self.page.views.append(PageNotFound(self.page))

        self.page.update()

    async def view_pop(self, e):
        """Called by page.on_view_pop. Must be async in Flet 0.81+."""
        if e.view is not None:
            self.page.views.remove(e.view)
        top_view = self.page.views[-1]
        await self.page.push_route(top_view.route)
