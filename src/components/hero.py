import flet as ft
import flet.canvas as cv

from utils import Config, supabase

from . import ChatMock


class Hero(ft.ResponsiveRow):
    def __init__(self, font_size: int, logged: bool = False):
        super().__init__(
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
            run_spacing=10,
        )

        self.logged = True
        self.font_size = font_size
        self.span_y = font_size * 1.1
        self.title_y = 0

        self.title_canvas = cv.Canvas(
            width=float("inf"),
            shapes=[],
        )
        self.title_canvas.height = font_size * 1.1 * 2 + font_size * 0.5
        self.title_canvas.shapes = self._make_title_shapes(
            0, self.title_y, font_size
        ) + self._make_span_shapes(0, self.span_y, font_size)

        self.left_container = ft.Container(
            height=320,
            col={
                ft.ResponsiveRowBreakpoint.XS: 10,
                ft.ResponsiveRowBreakpoint.MD: 7,
                ft.ResponsiveRowBreakpoint.LG: 5,
            },
            margin=ft.Margin.only(top=25),
            content=ft.Column(
                [
                    self.title_canvas,
                    ft.ResponsiveRow(
                        [
                            ft.Text(
                                "Transform static PDFs, Docx, and Text files into interactive conversations with our advanced RAG AI. Get instant answers with precise citations.",
                                style=ft.TextStyle(
                                    size=20,
                                    color=ft.Colors.with_opacity(
                                        0.65, ft.Colors.ON_SURFACE
                                    ),
                                    font_family=Config.FONT,
                                ),
                            ),
                        ],
                        width=400,
                    ),
                    ft.Row(
                        [
                            ft.Button(
                                "Start Now",
                                height=40,
                                margin=ft.Margin.only(top=10),
                                style=ft.ButtonStyle(
                                    shape=ft.ContinuousRectangleBorder(radius=10)
                                ),
                                bgcolor="#13DAEC",
                                on_click=self.go_to_session,
                            ),
                            *(
                                [
                                    ft.Button(
                                        "Login to Save History",
                                        height=40,
                                        margin=ft.Margin.only(top=10),
                                        style=ft.ButtonStyle(
                                            shape=ft.ContinuousRectangleBorder(
                                                radius=10
                                            )
                                        ),
                                        on_click=self.login,
                                    ),
                                ]
                                if not self.logged
                                else []
                            ),
                        ]
                    ),
                ],
                spacing=8,
                tight=True,
            ),
        )

        self.right_container = ft.Card(
            col={
                ft.ResponsiveRowBreakpoint.XS: 10,
                ft.ResponsiveRowBreakpoint.MD: 7,
                ft.ResponsiveRowBreakpoint.LG: 5,
            },
            height=390,
            elevation=10,
            bgcolor=Config.GREY_BG,
            content=ChatMock(),
        )

        self.controls = [
            self.left_container,
            self.right_container,
        ]

    def rebuild_shapes(self, size: float):
        title_y = 0
        span_y = size * 1.1  # second line
        self.title_canvas.height = size * 1.1 * 2 + size * 0.5
        self.title_canvas.shapes = self._make_title_shapes(
            0, title_y, size
        ) + self._make_span_shapes(0, span_y, size)
        self.title_canvas.update()

    def on_canvas_resize(self):
        self.rebuild_shapes(self.font_size)

    def update_card(self):
        self.right_container.width = 400
        self.right_container.height = 300
        self.right_container.update()

    @staticmethod
    def _make_title_shapes(x: float, y: float, size: float) -> list:

        stroke = cv.Text(
            x=x,
            y=y,
            value="Chat With Your",
            style=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                font_family=Config.FONT,
                size=size,
                letter_spacing=2,
                height=1.2,
                foreground=ft.Paint(
                    stroke_width=size * 0.05,
                    color=ft.Colors.PRIMARY,
                    stroke_join=ft.StrokeJoin.ROUND,
                    stroke_cap=ft.StrokeCap.ROUND,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
        )

        fill = cv.Text(
            x=x,
            y=y,
            value="Chat With Your",
            style=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                font_family=Config.FONT,
                size=size,
                letter_spacing=2,
                height=1.2,
                foreground=ft.Paint(
                    color=ft.Colors.PRIMARY,
                ),
            ),
        )
        return [stroke, fill]

    @staticmethod
    def _make_span_shapes(x: float, y: float, size: float) -> list:
        # Pass 1: thick stroke in a darker shade of Primary for added weight

        stroke = cv.Text(
            x=x,
            y=y,
            value="Documents",
            style=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                font_family=Config.FONT,
                size=size,
                letter_spacing=1,
                height=1.1,
                foreground=ft.Paint(
                    color="#2a9ab8",
                    stroke_width=size * 0.06,
                    stroke_join=ft.StrokeJoin.ROUND,
                    stroke_cap=ft.StrokeCap.ROUND,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
        )
        # Pass 2: solid fill
        fill = cv.Text(
            x=x,
            y=y,
            value="Documents",
            style=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                font_family=Config.FONT,
                size=size,
                letter_spacing=1,
                height=1.1,
                foreground=ft.Paint(color=Config.PRIMARY),
            ),
        )
        return [stroke, fill]

    async def go_to_session(self):
        await self.page.push_route("/chat")

    async def login(self):
        await self.page.push_route("/login")
