import random
import time

from .platform import windowMP
from .mouse_utils import (
    move_mouse_and_click,
    move_mouse,
    mouse_position,
    mouse_click,
    mouse_scroll,
    mouse_range,
)

from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .settings import settings_dict, jposition
from .game import waitForItOrPass

import logging

log = logging.getLogger(__name__)


def look_at_campfire_completed_tasks():
    """Once opened, look at campfire if you find completed tasks and, if so, open them"""

    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        while find_ellement(UIElement.campfire.filename, Action.screenshot):
            waitForItOrPass(Button.campfire_completed_task, 5)
            if find_ellement(Button.campfire_completed_task.filename, Action.move_and_click):
                while not find_ellement(Button.campfire_claim.filename, Action.move_and_click):
                    time.sleep(0.5)
                   
                while not find_ellement(UIElement.campfire.filename, Action.screenshot):
                    mouse_click()
                    time.sleep(1)
            else:
                break
    
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.25, windowMP()[3] / 2)
    
