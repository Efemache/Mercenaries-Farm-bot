import sys
import time

import os
import pathlib

from .image_utils import find_ellement
from .constants import Button, Action, UIElement
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


def selectGroup():
    """Look for the mercenaries group 'Botwork' and select it
    (click on 'LockIn' if necessary)"""

    log.debug("selectGroup : entering")

    # bad code but easily works
    # need to change it later to have a better solution
    group_name_custom = pathlib.PurePath(
        "conf/user/", Button.group_name.filename
    ).as_posix()

    group_name = (
        f"../../{group_name_custom}"
        if os.path.exists(group_name_custom)
        else Button.group_name.filename
    )
    # end of the section to replace #

    if find_ellement(group_name, Action.move_and_click):
        find_ellement(Button.choose_team.filename, Action.move_and_click)
        move_mouse(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2)
        waitForItOrPass(Button.lockin, 3)
        find_ellement(Button.lockin.filename, Action.move_and_click)

    log.debug("selectGroup : ended")
    return


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
