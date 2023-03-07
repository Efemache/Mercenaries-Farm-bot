import time
import logging
import pyautogui

from .base import WindowMgr
from ..platforms import find_os

# from ...exceptions import WindowManagerError

log = logging.getLogger(__name__)
try:
    import pgi

    pgi.install_as_gi()
    import gi

    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck, Gtk
except ImportError:
    if find_os() == "linux":
        log.error("gi.repository and/or pgi not installed")


class WindowMgrLinux(WindowMgr):
    """Encapsulates some calls for Linux window management"""

    def __init__(self):
        """Constructor"""
        self.win = None

    def find_game(self, WINDOW_NAME):
        """find the hearthstone game window"""
        screenHW = Wnck.Screen.get_default()
        while Gtk.events_pending():
            Gtk.main_iteration()
        windows = screenHW.get_windows()

        win = None
        for w in windows:
            if w.get_name() == WINDOW_NAME:
                win = w
                win.activate(int(time.time()))
                win.make_above()
                win.unmake_above()
                break
        if not win:
            print(f"No '{WINDOW_NAME}' window found.")
        self._win = win
        return win

    def get_window_geometry(self):
        # workaround for Battle.net
        if self._win.get_name() == "Battle.net":
            (width, height) = pyautogui.size()
            return (0, 0, width, height)
        else:
            return self._win.get_client_window_geometry()
