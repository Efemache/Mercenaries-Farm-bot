#! /usr/bin/env python3
import time
import sys

from modules.gameloop import where
from modules.battlenetloop import enter_from_battlenet
from modules.platforms import win
from modules.resolution import gen_images_new_resolution

import logging

log = logging.getLogger(__name__)


def main():
    log.info(f"Python version: {sys.version}")
    gen_images_new_resolution()
    #Sometimes it is the first BN window shall be launched, sometimes it is the second.
    BNCount=1

    while True:
        log.info("Loop")
        try:
            if win.find_game("Hearthstone"):
                where()
                BNCount=1
            elif win.find_game("Battle.net", BNCount):
                enter_from_battlenet()
                if BNCount==0:
                    BNCount=1
                else: 
                    BNCount=0
                time.sleep(1)
        except KeyboardInterrupt as kerr:
            log.info("Keyboard Interrupt %s", kerr)
            sys.exit(0)
        except Exception as error:
            log.error("Error: %s", error)
            time.sleep(1)


if __name__ == "__main__":
    main()
