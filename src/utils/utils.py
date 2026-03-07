from enum import Enum

from utils import Config


class Breakpoint:
    MOBILE_BREAKPOINT = 600
    LAPTOP_BREAKPOINT = 1200


class ScreenSize(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


class Responsive:
    _last_width: int | None = None
    _last_breakpoint: ScreenSize | None = None

    @staticmethod
    def screen(w: int) -> ScreenSize:
        if w <= 0:
            raise ValueError("Width must be positive")

        if w < Breakpoint.MOBILE_BREAKPOINT:
            return ScreenSize.MOBILE
        elif w < Breakpoint.LAPTOP_BREAKPOINT:
            return ScreenSize.TABLET
        else:
            return ScreenSize.DESKTOP

    @staticmethod
    def crossed_breakpoint(w: int) -> bool:
        """Returns True only if user switched between mobile/tablet/desktop."""
        new_breakpoint = Responsive.screen(w)

        if Responsive._last_breakpoint is None:
            Responsive._last_breakpoint = new_breakpoint
            return False

        if new_breakpoint != Responsive._last_breakpoint:
            Responsive._last_breakpoint = new_breakpoint
            return True

        return False

    @staticmethod
    def get_size() -> dict:

        if Responsive._last_breakpoint == ScreenSize.MOBILE:
            return Config.mobile
        elif Responsive._last_breakpoint == ScreenSize.TABLET:
            return Config.tablet
        else:
            return Config.desktop
