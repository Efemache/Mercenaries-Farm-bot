# import random
import time

from .platforms import windowMP
from .mouse_utils import (
    move_mouse_and_click,
    move_mouse,
    mouse_click,
)

from .constants import UIElement, Button, Action
from .image_utils import find_ellement

# from .settings import settings_dict, jposition
from .game import waitForItOrPass

import logging

log = logging.getLogger(__name__)

# To do : add an option in settings.ini to take screenshots (boolean)
#           for rewards and completed tasks
# To do : add mouse position in positions.json


def look_at_campfire_completed_tasks():
    """Once opened, look at campfire if you find completed tasks and,
    if so, open them.
    """

    retour = False
    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        retour = True
        while find_ellement(UIElement.campfire.filename, Action.move):
            waitForItOrPass(Button.campfire_completed_task, 5)
            if (
                find_ellement(
                    Button.campfire_completed_task.filename, Action.move_and_click
                )
                or find_ellement(
                    Button.campfire_completed_eventtask.filename, Action.move_and_click
                )
                or find_ellement(
                    Button.campfire_completed_expansiontask.filename,
                    Action.move_and_click,
                )
            ):
                # time.sleep(2)
                while not find_ellement(
                    Button.campfire_claim.filename, Action.screenshot
                ):
                    time.sleep(0.5)

                # Loop added beause sometimes the bot find the button but
                # Hearthstone is not ready, so the bot click too soon.
                # Need to make a loop to try several time to click
                while find_ellement(
                    Button.campfire_claim.filename, Action.move_and_click
                ):
                    time.sleep(0.5)
                    move_mouse(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.125)

                time.sleep(2)
                while not find_ellement(UIElement.campfire.filename, Action.screenshot):
                    mouse_click()
                    time.sleep(2)
            else:
                break

        move_mouse_and_click(windowMP(), windowMP()[2] / 1.16, windowMP()[3] / 1.93)

    return retour
