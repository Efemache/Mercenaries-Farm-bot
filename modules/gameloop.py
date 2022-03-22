import time

from .bounty import travelpointSelection, travelToLevel, goToEncounter, nextlvl
from .encounter import selectCardsInHand
from .constants import UIElement, Button, Checker, Action
from .image_utils import find_ellement
from .game import selectGroup


def where():
    """Try to enter in Mercenaries mode,
    detect where the bot have to resume and go for it"""
    # global threshold
    # tempthreshold = threshold

    find_ellement(Button.join_button.filename, Action.move_and_click)

    if find_ellement(Checker.menu.filename, Action.screenshot):  # chekers 21: 'menu'
        time.sleep(4)
        # Find PVE adventure payed and free
        find_ellement(
            UIElement.battle.filename, Action.move_and_click
        ) or find_ellement(UIElement.free_battle.filename, Action.move_and_click)

    # threshold = 0.6
    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):
        # threshold = tempthreshold
        time.sleep(3)
        # Find the travel point and the mode (normal/heroic)
        travelpointSelection()
        time.sleep(3)
    # threshold = tempthreshold

    # threshold = 0.65
    if find_ellement(UIElement.bounties.filename, Action.screenshot):
        time.sleep(3)
        # threshold = tempthreshold
        travelToLevel()
        time.sleep(3)
    # threshold = tempthreshold

    # threshold = 0.6
    if find_ellement(UIElement.choose_team.filename, Action.screenshot):
        time.sleep(3)
        # threshold = tempthreshold
        selectGroup()
        time.sleep(3)
    # threshold = tempthreshold

    # threshold = 0.95
    if find_ellement(Button.play.filename, Action.screenshot):
        time.sleep(3)
        # threshold = tempthreshold
        goToEncounter()
        time.sleep(3)
    # threshold = tempthreshold

    if find_ellement(UIElement.view_party.filename, Action.screenshot):
        nextlvl()

    if find_ellement(Button.num.filename, Action.screenshot):
        selectCardsInHand()

    return True
