import re
import logging
from ..base import WindowMgr
from ...platforms import find_os

log = logging.getLogger(__name__)

try:
    import win32gui
    import win32com.client as win32
    from win32api import GetSystemMetrics

    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    if find_os() == "windows":
        log.debug("win32gui not installed")

SW_SHOW = 5
shell = win32.Dispatch("WScript.Shell")


class WindowMgrWindowsWin32Gui(WindowMgr):
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_game(self, WINDOW_NAME, BNCount=0):
        """find the hearthstone game window"""
        self._find_window(WINDOW_NAME, BNCount)
        if (self._handle is not None) & (
            WINDOW_NAME != win32gui.GetWindowText(win32gui.GetForegroundWindow())
        ):
            self._show_window()
            self._set_foreground()
        return self._handle

    def get_window_geometry(self):
        global left, top, width, height
        # To get the active window name
        WINDOW_NAME = win32gui.GetWindowText(win32gui.GetForegroundWindow())

        # Judge which window, fake the BN resolution
        if WINDOW_NAME == "Battle.net":
            return (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
        else:
            left, top, width, height = win32gui.GetClientRect(self._handle)
            left, top = win32gui.ClientToScreen(self._handle, (left, top))
            return (left, top, width, height)

    def _window_enum_callback(self, hwnd, WINDOW_NAME):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(WINDOW_NAME, str(win32gui.GetWindowText(hwnd))) is not None:
            # print(hwnd)
            self._handles.append(hwnd)
            self._handle = hwnd
            print(self._handle)

    def _find_window(self, WINDOW_NAME, BNCount):
        self._handle = None
        self._handles = []
        win32gui.EnumWindows(self._window_enum_callback, WINDOW_NAME)

        if len(self._handles) < 1:
            log.info("Matched no window")
            return False
        if len(self._handles) > 1:
            print(BNCount)
            self._handle = self._handles[BNCount]
            print(self._handle)
        else:  # len(self._handles) == 1:
            self._handle = self._handles[0]

    def _show_window(self):
        shell.SendKeys("%")
        win32gui.ShowWindow(self._handle, SW_SHOW)

    def _set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
        shell.SendKeys("%")
