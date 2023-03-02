import time
import logging

from .base import WindowMgr
from ..platforms import find_os
from ...exceptions import WindowManagerError
from ...settings import settings_dict

log = logging.getLogger(__name__)
try:
    import pgi
    pgi.install_as_gi()
    import gi

    gi.require_version("Wnck", "3.0")
    from gi.repository import Wnck, Gtk
except ImportError:
    if find_os()=="linux":
        log.error("gi.repository and/or pgi not installed")

left = 0
top = 0
width = 1920
height = 1080

class WindowMgrLinux(WindowMgr):
    """Encapsulates some calls for Linux window management"""

    def __init__(self):
        """Constructor"""
        self.win = None

    def find_game(self, LINUX_NAME_WINDOWS):
        """find the hearthstone game window"""
        screenHW = Wnck.Screen.get_default()
        while Gtk.events_pending():
            Gtk.main_iteration()
        windows = screenHW.get_windows()

        win = None
        for w in windows:
            if w.get_name() == LINUX_NAME_WINDOWS:
                win = w
                # Not sure if you need those two lines, they are needed 
                # in Windows, to switch the active windows
                #shell = win32.Dispatch("WScript.Shell") 
                #shell.SendKeys('%')
                win.activate(int(time.time()))
                win.make_above()
                win.unmake_above()
                break
        if not win:
            raise WindowManagerError("No 'Hearthstone/Battle.net' window found.")
        self._win = win
        return win

    def get_window_geometry(self):
        global left, top, width, height

        #To get the acitve window name
        scr = Wnck.Screen.get_default()
        scr.force_update()
        CURRENT_NAME_WINDOWS = scr.get_active_window().get_name()

        #Judge which window, fake the BN resolution
        if CURRENT_NAME_WINDOWS == "Hearthstone":
            left, top, width, height = self._win.get_client_window_geometry()
        elif CURRENT_NAME_WINDOWS == "Battle.net":
            current_resolution = settings_dict["resolution"]
            ox, oy = current_resolution.split("x")
            width = int(ox)
            height = int(oy)
            left = 0
            top = 0
        else:
            log.info(WINDOW_NAME)
        return (left, top, width, height)
