import asyncio

import flet as ft

from views import HomePage, SessionMode


class RouteHandler:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.db = db

    def route(self, e=None):
        """Called directly on the startup or passed to page.on_route_change."""
        self.page.views.clear()

        match self.page.route:
            # case "/login":
            #     self.page.views.append(views.Login(self.page, self.db))
            #
            # case "/password":
            #     self.page.views.append(views.Password(self.page, self.db))
            #
            # case "/register":
            #     self.page.views.append(views.Register(self.page, self.db))

            case "/":
                self.page.views.append(HomePage(page=self.page))

            case "/session":
                self.page.views.append(SessionMode(page=self.page))
            #
            # case "/delete":
            #     self.page.views.append(views.Delete(self.page, self.db))
            #
            # case "/update":
            #     self.page.views.append(views.Update(self.page, self.db))
            #
            # case "/settings":
            #     self.page.views.append(views.Settings(self.page))
            #
            # case _:
            #     self.page.views.append(views.NotFoundPage(self.page))

        self.page.update()

    async def view_pop(self, e):
        """Called by page.on_view_pop. Must be async in Flet 0.81+."""
        if e.view is not None:
            self.page.views.remove(e.view)
        top_view = self.page.views[-1]
        await self.page.push_route(top_view.route)
