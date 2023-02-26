import time
from .constants import Button, Action
from .image_utils import find_ellement
from .game import defaultCase
import logging


log = logging.getLogger(__name__)

def enter_from_battlenet():
    find_ellement(Button.battlenet.filename, Action.move_and_click)

    try:
        find_ellement(Button.battlenet_hearthstone.filename, Action.move_and_click)
    except:
        time.sleep(1)

    if find_ellement(Button.battlenet_play.filename, Action.move_and_click):
        time.sleep(10)
        log.info("Wait for game start")

    else:
        log.info("Wait for play button to be available")
        defaultCase()
        time.sleep(3)

    return True
