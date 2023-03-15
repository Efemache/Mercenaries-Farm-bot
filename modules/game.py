import sys
import time

from .image_utils import find_ellement
from .constants import Action, UIElement, Button
from .settings import jposition
from .mouse_utils import move_mouse, move_mouse_and_click, mouse_position
from .platforms import windowMP

import logging

log = logging.getLogger(__name__)


def countdown(t, step=1, msg="Sleeping"):
    """Wait and show how many seconds til the end"""
    pad_str = " " * len("%d" % step)
    for i in range(t, 0, -step):
        sys.stdout.write(
            "%s for the next %d seconds %s\r" % (msg, i, pad_str),
        )
        time.sleep(step)


def waitForItOrPass(image, duration, step=0.5):
    """Wait to find 'image' on screen during 'duration' seconds (max)
    and continue if you don't find it.
    The purpose is to permit to find a particular part in Hearthstone
    but if the bot doesn't find it, try to go further
    if you can find another part that it could recognize
    """
    retour = False

    log.info(f"Waiting ({str(duration)}s max) for : {image}")
    for _ in range(int(duration / step)):
        time.sleep(step)
        # time.sleep(0.5)
        if find_ellement(image.filename, Action.screenshot):
            retour = True
            break

    return retour


def defaultCase():
    """Clicking on the right edge of the screen to click away popups"""
    """Saving x,y to move back into previous position"""
    if find_ellement(UIElement.quests.filename, Action.screenshot) or find_ellement(
        UIElement.encounter_card.filename, Action.screenshot
    ):
        x, y = mouse_position(windowMP())
        log.info("Trying to skip quests screen.")
        mx = jposition["mouse.neutral.x"]
        my = jposition["mouse.neutral.y"]
        move_mouse_and_click(windowMP(), windowMP()[2] / mx, windowMP()[3] / my)
        move_mouse(windowMP(), x, y)
    elif find_ellement(Button.reconnect.filename, Action.move_and_click):
        # Handle the disconnect case
        log.info("Game disconnected")
    else:
        # Click somewhere, quit?
        x, y = mouse_position(windowMP())
        log.info("Trying to skip quests screen.")
        mx = jposition["mouse.neutral.x"]
        my = jposition["mouse.neutral.y"]
        move_mouse_and_click(windowMP(), windowMP()[2] / mx, windowMP()[3] / my)
        time.sleep(30)
