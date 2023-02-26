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

    
    while True:
        log.info("Loop")
        try:
            if win.find_game("Hearthstone"):
                where()
#            if win.find_game("Battle.net"):
#                log.info("Battle.net found")
#                try:
#                   if win.find_game("Hearthstone"):
#                        log.info("Hearthstone found")
#                        where()
#                except:
#                    log.info("Hearthstone not found, enter from Battle.net")
#                    enter_from_battlenet()
#            else:
#                if win.find_game("Hearthstone"):
#                    log.info("Hearthstone found, without Battle.net")
#                    where()
        except KeyboardInterrupt as kerr:
            log.info("Keyboard Interrupt %s", kerr)
            sys.exit(0)
        except Exception as error:
            log.error("Error: %s", error)
            time.sleep(1)


if __name__ == "__main__":
    main()
