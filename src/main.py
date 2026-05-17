import flet as ft

from app.App import main
from utils import setup_logging

if __name__ == "__main__":
    setup_logging()
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8080)
