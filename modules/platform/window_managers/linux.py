import time
import logging

from .base import WindowMgr

log = logging.getLogger(__name__)
try:
    import gi

    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck, Gtk
except ImportError:
    log.info("gi.repository not installed")


class WindowMgrLinux(WindowMgr):
    """Encapsulates some calls for Linux window management"""

    def __init__(self):
        """Constructor"""
        self.win = None

    def find_game(self):
        """find the hearthstone game window"""
        screenHW = Wnck.Screen.get_default()
        while Gtk.events_pending():
            Gtk.main_iteration()
        windows = screenHW.get_windows()

        for w in windows:
            if w.get_name() == "Hearthstone":
                win = w
                win.activate(int(time.time()))
                win.make_above()
                win.unmake_above()
                break
        self._win = win
        return win

    def get_window_geometry(self):
        return self._win.get_client_window_geometry()
