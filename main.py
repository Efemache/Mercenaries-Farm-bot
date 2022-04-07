#! /usr/bin/env python3
import time

from modules.gameloop import where
from modules.platform import win

import logging

log = logging.getLogger(__name__)


def main():
    log.info("start")
    while True:
        log.info("Loop")
        try:
            if win.find_game():
                where()
        except Exception as error:
            log.error(f"Error: {error}")
            time.sleep(1)


if __name__ == "__main__":
    main()
