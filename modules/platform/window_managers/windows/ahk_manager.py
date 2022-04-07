import logging

from ..base import WindowMgr

log = logging.getLogger(__name__)

try:
    from ahk import AHK

    HAS_AHK = True
except ImportError:
    HAS_AHK = False
    log.warning("AHK Not Installed")


HEARHTSTONE_WINDOW_NAME_WINDOWS = "Hearthstone"


class WindowMgrWindowsAHK(WindowMgr):
    """Encapsulates some calls to AHK for window management"""

    def __init__(self):
        """Constructor"""
        self._win = None
        self._ahk = AHK()

    def find_game(self):
        """find the hearthstone game window"""
        win = self._ahk.win_get(title=HEARHTSTONE_WINDOW_NAME_WINDOWS)
        win.show()
        win.to_top()
        win.activate()
        self._win = win
        return self._win

    def get_window_geometry(self):
        return self._win.rect
