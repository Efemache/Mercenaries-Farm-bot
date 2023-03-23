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


def toggle_campfire_screen():
    if find_ellement(Button.campfire_hiddenparty.filename, Action.move_and_click):
        return "party"
        time.sleep(2)
    elif find_ellement(Button.campfire_hiddenvisitors.filename, Action.move_and_click):
        return "visitor"
        time.sleep(2)
    else:
        return None


def check_party_tasks():
    if find_ellement(Button.campfire_hiddenvisitors.filename, Action.screenshot):
        waitForItOrPass(Button.campfire_completed_partytask, 3)
        if find_ellement(
            Button.campfire_completed_partytask.filename, Action.move_and_click
        ):
            for x in range(60):
                if not find_ellement(Button.campfire_claim.filename, Action.screenshot):
                    time.sleep(0.5)
                else:
                    break
            return True
    return False


def check_visitor_tasks():
    if find_ellement(Button.campfire_hiddenparty.filename, Action.screenshot):
        waitForItOrPass(Button.campfire_completed_task, 3)
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
            return True
    return False


def claim_task_reward():
    for x in range(60):
        if not find_ellement(Button.campfire_claim.filename, Action.screenshot):
            time.sleep(0.5)
        else:
            break

    # Loop added beause sometimes the bot find the button but
    # Hearthstone is not ready, so the bot click too soon.
    # Need to make a loop to try several time to click
    for x in range(60):
        if find_ellement(Button.campfire_claim.filename, Action.move_and_click):
            time.sleep(0.5)
            move_mouse(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.125)
        else:
            break

    time.sleep(2)
    for x in range(60):
        if not find_ellement(UIElement.campfire.filename, Action.screenshot):
            mouse_click()
            time.sleep(2)
        else:
            break


def look_at_campfire_completed_tasks():
    """Once opened, look at campfire if you find completed tasks and,
    if so, open them.
    """

    retour = False
    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        retour = True
        toggled = False
        for x in range(60):
            if find_ellement(UIElement.campfire.filename, Action.move):
                if (
                    find_ellement(Button.campfire_hiddenparty.filename, Action.screenshot)
                    and check_visitor_tasks()
                ) or (
                    find_ellement(
                        Button.campfire_hiddenvisitors.filename, Action.screenshot
                    )
                    and check_party_tasks()
                ):
                    claim_task_reward()
                else:
                    if toggled:
                        break
                    else:
                        toggle_campfire_screen()
                        toggled = True
            else:
                break

        move_mouse_and_click(windowMP(), windowMP()[2] / 1.16, windowMP()[3] / 1.93)

    return retour
