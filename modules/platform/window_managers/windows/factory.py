import logging

from .win32gui_manager import WindowMgrWindowsWin32Gui, HAS_WIN32GUI
from .ahk_manager import WindowMgrWindowsAHK, HAS_AHK

log = logging.getLogger(__name__)


def get_window_mgr_on_windows():
    if HAS_WIN32GUI:
        return WindowMgrWindowsWin32Gui
    elif HAS_AHK:
        return WindowMgrWindowsAHK
    else:
        log.error("No Window Manager found for Windows")
