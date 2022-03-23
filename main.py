#! /usr/bin/env python3
import time

from modules.gameloop import where
from modules.platform import find_os, findgame


def main():
    print("start")
    try:
        myOS = find_os()
        findgame(myOS)
        while True:
            print("Loop")
            if findgame(myOS):
                where()
            else:
                print("Game window not found.")
                time.sleep(1)
    except Exception as E:
        print("Error", E)


if __name__ == "__main__":
    main()
