from enum import Enum

import flet as ft

from utils import Config


def app_redirect_url(page: ft.Page, path: str = "") -> str:
    """Build an HTTP (S) URL from page.url, which Flet returns as ws(s)://.
    `path` should start with "/" if non-empty (e.g. "/auth/callback").
    """
    raw = (page.url or "").rstrip("/")
    if raw.startswith("ws://"):
        raw = "http://" + raw[len("ws://") :]  # noqa
    elif raw.startswith("wss://"):
        raw = "https://" + raw[len("wss://") :]
    return f"{raw}{path}"


class Breakpoint:
    MOBILE_BREAKPOINT = 1024
    LAPTOP_BREAKPOINT = 1200


class ScreenSize(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


class Responsive:
    _last_width: int | None = None
    _last_breakpoint: ScreenSize | None = None

    @staticmethod
    def screen(w: int | float) -> ScreenSize:
        if w <= 0:
            raise ValueError("Width must be positive")

        if w < Breakpoint.MOBILE_BREAKPOINT:
            return ScreenSize.MOBILE
        elif w < Breakpoint.LAPTOP_BREAKPOINT:
            return ScreenSize.TABLET
        else:
            return ScreenSize.DESKTOP

    @staticmethod
    def crossed_breakpoint(w: int | float) -> bool:
        """Returns True only if a user switched between mobile/tablet/desktop."""
        new_breakpoint = Responsive.screen(w)

        if Responsive._last_breakpoint is None:
            Responsive._last_breakpoint = new_breakpoint
            return False

        if new_breakpoint != Responsive._last_breakpoint:
            Responsive._last_breakpoint = new_breakpoint
            return True

        return False

    @staticmethod
    def get_size(width: int | float | None = None) -> dict:
        if width and width > 0:
            Responsive._last_breakpoint = Responsive.screen(width)

        if Responsive._last_breakpoint == ScreenSize.MOBILE:
            return Config.mobile
        elif Responsive._last_breakpoint == ScreenSize.TABLET:
            return Config.tablet
        else:
            return Config.desktop
