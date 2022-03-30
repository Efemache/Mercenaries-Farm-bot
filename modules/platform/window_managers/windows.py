import logging

from .base import WindowMgr

log = logging.getLogger(__name__)

try:
    import win32gui

    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    log.warning("win32gui not installed")

try:
    from ahk import AHK

    HAS_AHK = True
except ImportError:
    HAS_AHK = False
    log.warning("AHK Not Installed")


HEARHTSTONE_WINDOW_NAME_WINDOWS = "Hearthstone"
SW_SHOW = 5


class WindowMgrWindows(WindowMgr):
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
        return win32gui.GetWindowRect(self._handle)

    def _find_window(self):
        self._handle = win32gui.FindWindow(None, HEARHTSTONE_WINDOW_NAME_WINDOWS)

    def _show_window(self):
        win32gui.ShowWindow(self._handle, SW_SHOW)

    def _set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


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


def get_window_mgr_on_windows():
    if HAS_WIN32GUI:
        return WindowMgrWindows
    elif HAS_AHK:
        return WindowMgrWindowsAHK
    else:
        log.error("No Window Manager found for Windows")
