import sys
import time


def find_os():
    # try to detect the OS (Windows, Linux, Mac, ...)
    # to load specific libs
    if sys.platform in ["Windows", "win32", "cygwin"]:
        myOS = "windows"
    elif sys.platform in ["linux", "linux2"]:
        myOS = "linux"
    else:
        myOS = "unknown"
        print("sys.platform='{platform}' is unknown.".format(platform=sys.platform))
        exit(1)
    return myOS


def windowMP():
    """window multi-platorms (Windows & Linux support)"""
    if myOS == "linux":
        return get_window_geometry_on_linux()
    elif myOS == "windows":
        return get_window_geometry_on_windows()
    else:
        return None


def get_window_geometry_on_linux():
    return win.get_client_window_geometry()


def get_window_geometry_on_windows():
    return win.rect


def findgame(myOS):
    """look for Hearthstone window for Windows or Linux"""
    win = None

    try:
        if myOS == "linux":
            win = find_game_on_linux()
        elif myOS == "windows":
            win = find_game_on_windows()
        else:
            print("OS not supported.")
    except Exception:
        print("No game found.")
    return win


def find_game_on_linux():
    try:
        import gi

        gi.require_version("Wnck", "3.0")
        from gi.repository import Wnck, Gtk
    except ImportError:
        print("gi.repository not installed")

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
    return win


def find_game_on_windows():
    try:
        from ahk import AHK

        ahk = AHK()
    except ImportError:
        print("ahk not installed")
    win = ahk.win_get(title="Hearthstone")
    win.show()
    win.to_top()
    win.activate()
    return win


myOS = find_os()
win = findgame(myOS)
