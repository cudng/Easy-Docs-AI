# import flet as ft
#
# from utils import Config
#
#
# class ChatAppbar(ft.AppBar):
#     def __init__(
#         self, page: ft.Page, filename, margin_left: int, on_toggle_sources=None
#     ):
#         self.sources_shown = False
#         self.on_toggle_sources = on_toggle_sources
#         self.ref_page = page
#
#         super().__init__(
#             toolbar_height=60,
#             bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
#             leading=ft.Row(
#                 [
#                     # ft.VerticalDivider(
#                     #     color=ft.Colors.TRANSPARENT, width=margin_left
#                     # ),
#                     ft.Container(
#                         ft.Image(Config.SVG, color="#13DAEC"),  # noqa
#                         padding=ft.Padding.only(top=10, bottom=10, left=margin_left),
#                         on_click=self.go_home,
#                         ink=True,
#                     ),
#                     ft.Text(),
#                 ]
#             ),
#             #     on_click=self.go_home,
#             #     ink=True,
#             # ),
#             title=ft.Text(filename),
#             center_title=True,
#             actions=[
#                 self.sources_button,
#                 ft.Button(
#                     content="Login",
#                     color=ft.Colors.WHITE,
#                     height=40,
#                     bgcolor=Config.PRIMARY,
#                     style=ft.ButtonStyle(
#                         shape=ft.RoundedRectangleBorder(radius=8),
#                     ),
#                     margin=ft.Margin.only(right=20),
#                 ),
#             ],
#         )
#
#     def _toggle_sources(self, e=None):
#         self.sources_shown = not self.sources_shown
#         if self.sources_shown:
#             self.sources_button.content = "Hide Sources"
#             self.sources_button.icon = ft.Icons.VISIBILITY_OFF
#         else:
#             self.sources_button.content = "Show Sources"
#             self.sources_button.icon = ft.Icons.VISIBILITY
#         self.sources_button.update()
#         if self.on_toggle_sources:
#             self.on_toggle_sources(self.sources_shown)
#
#     def update_margin(self, w: int):
#         self.leading.controls[0].width = w
#
#     async def go_home(self):
#         await self.ref_page.push_route("/")
