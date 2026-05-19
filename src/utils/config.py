import flet as ft


class Config:
    PRIMARY = "#5BC8E8"
    TEAL = "#00BCD4"
    TEAL_DARK = "#0097A7"
    AI_PURPLE = "#7C3AED"
    ERROR = "#F44336"
    GREY_BG = ft.Colors.SURFACE_CONTAINER_LOWEST
    FONT = "Inter"
    DRAWER_WIDTH = 220
    DOC_ITEM_WIDTH = 280
    MAX_CHATS_PER_USER = 10
    MAX_FILE_SIZE_BYTES = (
        5 * 1024 * 1024
    )  # matches documents.size_bytes CHECK constraint
    MAX_FILE_SIZE_BYTES_GUEST = 2 * 1024 * 1024
    _NO_TRANSITIONS = ft.PageTransitionsTheme(
        android=ft.PageTransitionTheme.NONE,
        ios=ft.PageTransitionTheme.NONE,
        linux=ft.PageTransitionTheme.NONE,
        macos=ft.PageTransitionTheme.NONE,
        windows=ft.PageTransitionTheme.NONE,
    )
    THEME = ft.Theme(
        color_scheme=ft.ColorScheme(primary="#000000", on_primary="#FFFFFF"),
        page_transitions=_NO_TRANSITIONS,
    )
    DARK_THEME = ft.Theme(
        color_scheme=ft.ColorScheme(primary="#FFFFFF", on_primary="#000000"),
        page_transitions=_NO_TRANSITIONS,
    )
    SVG = """
        <svg fill="currentColor" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 4H17.3334V17.3334H30.6666V30.6666H44V44H4V4Z"/>
        </svg>
        """
    PAGE_FONTS = {
        "Inter": "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa2JL7SUc.woff2"
    }
    mobile: dict[str, int] = {
        "font_size": 35,
        "left_margin": 20,
        "top_margin": 20,
        "right_margin": 50,
        "list_padding": 20,
    }
    tablet: dict[str, int] = {
        "font_size": 45,
        "left_margin": 80,
        "top_margin": 50,
        "right_margin": 100,
        "list_padding": 50,
    }
    desktop: dict[str, int] = {
        "font_size": 60,
        "left_margin": 100,
        "top_margin": 100,
        "right_margin": 150,
        "list_padding": 150,
    }
