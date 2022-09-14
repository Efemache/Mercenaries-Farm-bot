import time
import sys

from .bounty import travelToLevel, goToEncounter
from .travelpoint import travelpointSelection
from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .game import selectGroup, defaultCase
from .campfire import look_at_campfire_completed_tasks
from .settings import jposition
from .mouse_utils import move_mouse
from .platforms import windowMP
from .resolution import check_resolution

import logging

log = logging.getLogger(__name__)


def where():
    """Try to enter in Mercenaries mode,
    detect where the bot have to resume and go for it"""

    # Check Hearthstone resolution and compare it to settings resolution
    _, _, width, height = windowMP()
    win_game_resolution = f"{width}x{height}"
    if not check_resolution(win_game_resolution):
        log.error(
            f"Game window size ({win_game_resolution}) doesn't match your settings."
        )
        sys.exit()

    find_ellement(Button.join_button.filename, Action.move_and_click)

    # Find PVE adventure payed and free
    if find_ellement(UIElement.battle.filename, Action.move_and_click) or find_ellement(
        UIElement.free_battle.filename, Action.move_and_click
    ):
        mx = jposition["mouse.neutral.x"]
        my = jposition["mouse.neutral.y"]
        move_mouse(windowMP(), windowMP()[2] / mx, windowMP()[3] / my)
    #        time.sleep(3)

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):
        #        time.sleep(3)
        # Find the travel point and the mode (normal/heroic)
        travelpointSelection()
    #        time.sleep(3)

    if find_ellement(UIElement.bounties.filename, Action.screenshot):
        #        time.sleep(3)
        travelToLevel()
        time.sleep(1)

    if find_ellement(UIElement.team_selection.filename, Action.screenshot):
        #        time.sleep(3)
        selectGroup()
        time.sleep(1)

    #    if find_ellement(Button.play.filename, Action.screenshot):
    #        time.sleep(3)
    #        goToEncounter()
    #        # time.sleep(3)

    #    if find_ellement(UIElement.view_party.filename, Action.screenshot):
    #        nextlvl()

    
    if find_ellement(UIElement.view_party.filename, Action.screenshot):
        goToEncounter()
    
    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        #        time.sleep(2)
        look_at_campfire_completed_tasks()
    #        time.sleep(3)

    # Note: feature disabled because of enemy board detection needing
    # to start log-scan before battle started
    # Note: could work if log scan had something like a rewind scan
    # if find_ellement(Button.num.filename, Action.screenshot):
    #     selectCardsInHand()

    else:
        defaultCase()
    #        time.sleep(3)

    return True
