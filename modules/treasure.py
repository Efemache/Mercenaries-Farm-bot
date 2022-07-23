import random
import time

from queue import PriorityQueue

from .platform import windowMP
from .mouse_utils import move_mouse_and_click
from .constants import Button, Action
from .image_utils import find_ellement
from .settings import treasures_priority

import logging

log = logging.getLogger(__name__)


def chooseTreasure():
    """used to choose a Treasure after a battle/fight
    note: Treasures are added to a queue (FIFO); if no matches are found a random treasure is selected.
    """
    treasures_queue = PriorityQueue()

    for treasure in treasures_priority:
        treasures_queue.put((treasures_priority[treasure], treasure))

    log.debug(f"treasures queue contains : {treasures_queue}")

    while not treasures_queue.empty():
        next_treasure = treasures_queue.get()[1]

        treasure = str(f"treasures/{next_treasure}.png")

        if find_ellement(treasure, Action.move_and_click):
            time.sleep(1)
            break
    else:
        log.info("No known treasure found: picking random one")
        temp = random.choice([2.3, 1.7, 1.4])
        y = windowMP()[3] // 2
        x = windowMP()[2] // temp
        move_mouse_and_click(windowMP(), x, y)
        time.sleep(1)
        # break

    while True:
        if find_ellement(Button.take.filename, Action.move_and_click):
            break
        if find_ellement(Button.keep.filename, Action.move_and_click):
            break
        if find_ellement(Button.replace.filename, Action.move_and_click):
            break
        time.sleep(1)
