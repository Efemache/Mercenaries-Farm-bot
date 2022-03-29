import sys


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
