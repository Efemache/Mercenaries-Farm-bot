#! /usr/bin/env python3
import time

# from tkinter import *
# from tkinter.ttk import *

from modules.settings import configread
from modules.gameloop import where
from modules.platform import find_os, findgame

# global threshold
global zoneLog
# threshold = 0.75
global mercslist
mercslist = {}
# global mercsAbilities
mercsAbilities = {}


# Settings -
# 0: MonitorResolution (1920x1080),
# 1: level (20),
# 2: location (The Barrens),
# 3: mode (Heroic),
# 4: quitBeforeBossFight (True),
# 5: heroSet (True),
# 6: GameDir (path)
setings = []
settings = {}


def main():
    print("start")
    try:
        myOS = find_os()
        configread()
        findgame(myOS)
        while True:
            print("Loop")
            if findgame(myOS):
                where()
            #                time.sleep(0.5)
            else:
                print("Game window not found.")
                time.sleep(1)
    except Exception as E:
        print("Error", E)


if __name__ == "__main__":
    main()
