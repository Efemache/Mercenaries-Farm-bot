#! /usr/bin/env python3
import time

from modules.gameloop import where
from modules.platform import win


def main():
    print("start")
    try:
        while True:
            print("Loop")
            if win.find_game():
                where()
            else:
                print("Game window not found.")
                time.sleep(1)
    except Exception as E:
        print("Error", E)


if __name__ == "__main__":
    main()
