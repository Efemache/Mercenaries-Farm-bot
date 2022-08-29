import logging

from ..base import WindowMgr
from ...platform import find_os

log = logging.getLogger(__name__)

try:
    import win32gui

    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    if find_os()=="windows":
        log.debug("win32gui not installed")


HEARHTSTONE_WINDOW_NAME_WINDOWS = "Hearthstone"
SW_SHOW = 5


class WindowMgrWindowsWin32Gui(WindowMgr):
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_game(self):
        """find the hearthstone game window"""
        self._find_window()
        self._show_window()
        self._set_foreground()
        return self._handle

    def get_window_geometry(self):
        left, top, width, height = win32gui.GetClientRect(self._handle)
        left, top = win32gui.ClientToScreen(self._handle, (left, top))
        return (left, top, width, height)

    def _find_window(self):
        self._handle = win32gui.FindWindow(None, HEARHTSTONE_WINDOW_NAME_WINDOWS)

    def _show_window(self):
        win32gui.ShowWindow(self._handle, SW_SHOW)

    def _set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
