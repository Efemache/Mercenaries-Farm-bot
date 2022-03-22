import time

from .image_utils import find_ellement
from .constants import Checker, Button, Action
from .debug import debug
from .mouse_utils import move_mouse
from .platform import windowMP


def waitForItOrPass(image, duration):
    """Wait to find 'image' on screen during 'duration' seconds (max)
    and continue if you don't find it.
    The purpose is to permit to find a particular part in Hearthstone
    but if the bot doesn't find it, try to go further
    if you can find another part that it could recognize
    """
    retour = False

    print(f"Waiting ({str(duration)}s max) for : ", image)
    for _ in range(duration * 2):
        time.sleep(0.5)
        if find_ellement(image.filename, Action.screenshot):
            retour = True
            break

    return retour


def selectGroup():
    """Look for the mercenaries group 'Botwork' and select it
    (click on 'LockIn' if necessary)"""
    # global threshold
    # tempthreshold = threshold
    print("selectGroup : entering")
    # threshold = 0.8

    if find_ellement(Checker.find.filename, Action.move_and_click):
        find_ellement(Button.start1.filename, Action.move_and_click)
        move_mouse(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2)
        waitForItOrPass(Button.lockin, 3)
        find_ellement(Button.lockin.filename, Action.move_and_click)

    # threshold = tempthreshold
    debug("selectGroup : ended")
    return
