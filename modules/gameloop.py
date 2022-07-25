import time

from .bounty import travelpointSelection, travelToLevel, goToEncounter, nextlvl
from .encounter import selectCardsInHand
from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .game import selectGroup, defaultCase
from .campfire import look_at_campfire_completed_tasks


def where():
    """Try to enter in Mercenaries mode,
    detect where the bot have to resume and go for it"""

    find_ellement(Button.join_button.filename, Action.move_and_click)

    if find_ellement(Button.tavern.filename, Action.screenshot):
        time.sleep(4)
        # Find PVE adventure payed and free
        find_ellement(
            UIElement.battle.filename, Action.move_and_click
        ) or find_ellement(UIElement.free_battle.filename, Action.move_and_click)
        time.sleep(3)

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):
        time.sleep(3)
        # Find the travel point and the mode (normal/heroic)
        travelpointSelection()
        time.sleep(3)

    if find_ellement(UIElement.bounties.filename, Action.screenshot):
        time.sleep(3)
        travelToLevel()
        time.sleep(3)

    if find_ellement(UIElement.team_selection.filename, Action.screenshot):
        time.sleep(3)
        selectGroup()
        time.sleep(3)

    if find_ellement(Button.play.filename, Action.screenshot):
        time.sleep(3)
        goToEncounter()
        # time.sleep(3)

    if find_ellement(UIElement.view_party.filename, Action.screenshot):
        nextlvl()

    if find_ellement(UIElement.campfire.filename, Action.screenshot):
        time.sleep(2)
        look_at_campfire_completed_tasks()
        time.sleep(3)

    # Note: feature disabled because of enemy board detection needing
    # to start log scan before battle starter
    # if find_ellement(Button.num.filename, Action.screenshot):
    #     selectCardsInHand()

    else:
        defaultCase()
        time.sleep(3)

    return True
