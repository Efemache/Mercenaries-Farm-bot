import logging
import re
import logging
import win32com.client as win32
from ..base import WindowMgr

log = logging.getLogger(__name__)

try:
    import win32gui

    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    if find_os()=="windows":
        log.debug("win32gui not installed")

SW_SHOW = 5

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_game(self, WINDOW_NAME_WINDOWS):
        """find the hearthstone game window"""
        self._find_window(WINDOW_NAME_WINDOWS)
        self._show_window()
        self._set_foreground()
        return self._handle

    def get_window_geometry(self):
        WINDOW_NAME = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if WINDOW_NAME == "Hearthstone":
            left, top, width, height = win32gui.GetClientRect(self._handle)
            left, top = win32gui.ClientToScreen(self._handle, (left, top))
        elif WINDOW_NAME == "Battle.net":
            left = 0
            top = 0
            width = 1920
            height = 1080
        else:
            log.info(WINDOW_NAME)
        return (left, top, width, height)

    def _window_enum_callback(self, hwnd, WINDOW_NAME_WINDOWS):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(WINDOW_NAME_WINDOWS, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handles.append(hwnd)
            self._handle = hwnd

    def _find_window(self, WINDOW_NAME_WINDOWS):
        self._handle = None
        self._handles = []
        win32gui.EnumWindows(self._window_enum_callback, WINDOW_NAME_WINDOWS)

        if len(self._handles) < 1:
            print("Matched no window")
            return False
        if len(self._handles) > 1:
            print("Selecting the first handle of multiple windows:")
            self._handle = self._handles[1]
        else: # len(self._handles) == 1:
            self._handle = self._handles[0]
            print("Matched a single window:")

    def _show_window(self):
        win32gui.ShowWindow(self._handle, SW_SHOW)

    def _set_foreground(self):
        """put the window in the foreground"""
        shell = win32.Dispatch("WScript.Shell") 
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._handle)