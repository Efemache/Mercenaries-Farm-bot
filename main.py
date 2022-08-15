#! /usr/bin/env python3
import time
import sys

from modules.gameloop import where
from modules.platform import win
from modules.generate_resolution import generate_temp_resolution

import logging

log = logging.getLogger(__name__)


def main():
    log.info(f"Python version: {sys.version}")
    found = False
    while True:
        log.info("Loop")
        try:
            if win.find_game():
                if not found:
                    found = True
                    log.info("Game found")
                    generate_temp_resolution()
                where()
        except KeyboardInterrupt as kerr:
            log.error("Keyboard Interrupt %s", kerr)
            sys.exit(0)
        except Exception as error:
            log.error("Error: %s", error)
            time.sleep(1)


if __name__ == "__main__":
    main()
