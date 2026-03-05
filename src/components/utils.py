# import flet as ft
#
#
# class LeftDivider(ft.Container):
#     def did_mount(self):
#         self.width = self._get_thickness()
#         self.bgcolor = ft.Colors.GREY_300
#         self.page.on_resize = self._on_resize
#         self.update()
#
#     def _get_thickness(self):
#         if self.page.width < 600:
#             return 20
#         elif self.page.width < 1200:
#             return 50
#         return 100
#
#     def _on_resize(self, e):
#         self.width = self._get_thickness()
#         self.update()
#
#
# # utils.py
# def register_resize(page: ft.Page, callback):
#     existing = page.on_resize
#
#     def handler(e):
#         if existing:
#             existing(e)
#         callback(e)
#
#     page.on_resize = handler
