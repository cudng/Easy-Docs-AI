import flet as ft


class Config:
    PRIMARY = "#5BC8E8"
    FONT = "Inter"
    THEME = ft.Theme(
        color_scheme=ft.ColorScheme(primary="#000000", on_primary="#FFFFFF")
    )
    DARK_THEME = ft.Theme(
        color_scheme=ft.ColorScheme(primary="#FFFFFF", on_primary="#000000")
    )
    SVG = """
        <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 4H17.3334V17.3334H30.6666V30.6666H44V44H4V4Z"/>
        </svg>
        """
    PAGE_FONTS = {
        "Inter": "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa2JL7SUc.woff2"
    }
    mobile: dict[str, int] = {"font_size": 30, "left_margin": 20, "top_margin": 50}
    tablet: dict[str, int] = {"font_size": 45, "left_margin": 100, "top_margin": 100}
    desktop: dict[str, int] = {"font_size": 60, "left_margin": 150, "top_margin": 100}
