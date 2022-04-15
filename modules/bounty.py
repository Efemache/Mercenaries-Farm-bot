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
from .settings import settings_dict, jposition, jthreshold
from .game import waitForItOrPass
from .encounter import selectCardsInHand
from .campfire import look_at_campfire_completed_tasks

import logging

log = logging.getLogger(__name__)


def collect():
    """Collect the rewards just after beating the final boss of this level"""

    # it's difficult to find every boxes with lib CV2 so,
    # we try to detect just one and then we click on all known positions
    while not find_ellement(Button.done.filename, Action.move_and_click):
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2.4)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.7, windowMP()[3] / 1.4)

        move_mouse_and_click(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2.7)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.7, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.6, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.8, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.9, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.4, windowMP()[3] / 1.3)
        time.sleep(1)

    # move the mouse to avoid a bug where the it is over a card/hero (at the end)
    # hiding the "OK" button
    move_mouse(windowMP(), windowMP()[2] // 1.25, windowMP()[3] // 1.25)
    # quit the bounty
    while not find_ellement(Button.finishok.filename, Action.move_and_click):
        time.sleep(1)
        mouse_click()
        time.sleep(0.5)


def quitBounty():
    end = False
    if find_ellement(Button.view_party.filename, Action.move_and_click):
        while not find_ellement(UIElement.your_party.filename, Action.move):
            time.sleep(0.5)
        while not find_ellement(Button.retire.filename, Action.move_and_click):
            time.sleep(0.5)
        while not find_ellement(Button.lockin.filename, Action.move_and_click):
            time.sleep(0.5)
        end = True
    return end


def nextlvl():
    """Progress on the map (Boon, Portal, ...) to find the next battle"""
    time.sleep(1.5)
    retour = True

    if not find_ellement(Button.play.filename, Action.screenshot):

        if find_ellement(UIElement.task_completed.filename, Action.screenshot):
            waitForItOrPass(UIElement.campfire, 10)
            look_at_campfire_completed_tasks()

        elif find_ellement(UIElement.campfire.filename, Action.screenshot):
            look_at_campfire_completed_tasks()
            time.sleep(3)

        elif find_ellement(Button.reveal.filename, Action.move_and_click):
            time.sleep(1)
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] // 1.25)
            time.sleep(1.5)

        elif find_ellement(Button.visit.filename, Action.move_and_click):
            y = windowMP()[3] // 2.2
            time.sleep(7)
            while find_ellement(UIElement.visitor.filename, Action.screenshot):
                if settings_dict["stopatstranger"]:
                    log.info("Stopping after meeting Mysterious Stranger")
                    exit(1)

                temp = random.choice([3, 2, 1.7])
                x = windowMP()[2] // temp

                move_mouse_and_click(windowMP(), x, y)

                time.sleep(0.2)
                find_ellement(Button.choose_task.filename, Action.move_and_click)
                time.sleep(3)
                mouse_click()
                time.sleep(8)

        elif find_ellement(
            Button.pick.filename, Action.move_and_click
        ) or find_ellement(Button.portal_warp.filename, Action.move_and_click):
            time.sleep(1)
            mouse_click()
            time.sleep(5)
        elif find_ellement(UIElement.mystery.filename, Action.screenshot):
            time.sleep(1)
            find_ellement(UIElement.mystery.filename, Action.move_and_click)

        elif find_ellement(UIElement.spirithealer.filename, Action.screenshot):
            time.sleep(1)
            find_ellement(UIElement.spirithealer.filename, Action.move_and_click)

        else:
            x, y = mouse_position(windowMP())
            log.debug(f"Mouse (x, y) : ({x}, {y})")
            if y >= (windowMP()[3] // 2.2 - mouse_range) and y <= (
                windowMP()[3] // 2.2 + mouse_range
            ):
                x += windowMP()[2] // 25
            else:
                x = windowMP()[2] // 3.7

            if x > windowMP()[2] // 1.5:
                log.debug("Didnt find a battle. Try to go 'back'")
                find_ellement(Button.back.filename, Action.move_and_click)
                retour = False
            else :
                y = windowMP()[3] // 2.2
                log.debug(f"move mouse to (x, y) : ({x}, {y})")
                move_mouse_and_click(windowMP(), x, y)

    return retour


def chooseTreasure():
    """used to choose a Treasure after a battle/fight
    Note: should be updated to select "good" (passive?) treasure instead of a random one
    """
    temp = random.choice([2.3, 1.7, 1.4])
    y = windowMP()[3] // 2
    x = windowMP()[2] // temp
    move_mouse_and_click(windowMP(), x, y)
    time.sleep(0.5)
    while True:
        if find_ellement(Button.take.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.keep.filename, Action.move_and_click):
            time.sleep(1)
            break
        if find_ellement(Button.replace.filename, Action.move_and_click):
            time.sleep(1)
            break


def travelpointSelection():
    """Choose a Travel Point (The Barrens, Felwood, ...)
    and the mode : Normal or Heroic
    """

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):

        move_mouse(windowMP(), windowMP()[2] // 1.5, windowMP()[3] // 2)

        mouse_scroll(jposition["travelpoint.scroll.top"])
        time.sleep(0.5)

        location = settings_dict["location"]
        tag = f"travelpoint.{location}.scroll"
        if location == "The Barrens":
            find_ellement(
                UIElement.Barrens.filename, 
                Action.move_and_click, 
                jthreshold["travelpoints"]
            )

        else:
            try:
                mouse_scroll(jposition[tag])
                move_mouse(windowMP(), windowMP()[2] // 3, windowMP()[3] // 2)
                time.sleep(0.5)
                find_ellement(
                    getattr(UIElement, location).filename, 
                    Action.move_and_click, 
                    jthreshold["travelpoints"]
                )
            except Exception:
                log.error(f"Travel Point unknown : {location}")

        move_mouse(windowMP(), windowMP()[2] // 2, windowMP()[3] // 2)
        time.sleep(0.5)

        if settings_dict["mode"] == "Normal":
            find_ellement(UIElement.normal.filename, Action.move_and_click)
        elif settings_dict["mode"] == "Heroic":
            find_ellement(UIElement.heroic.filename, Action.move_and_click)
        else:
            log.error("Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(Button.choose_travel, 2)
    find_ellement(Button.choose_travel.filename, Action.move_and_click)


def goToEncounter():
    """
    Start new fight,
    continue on the road and collect everything (treasure, rewards, ...)
    """
    log.info("goToEncounter : entering")
    time.sleep(2)
    travelEnd = False

    while not travelEnd:
        # ToDo : add a tempo when you detect a new completed task
        # if find (task completed) :
        #   time.sleep(2)

        if find_ellement(Button.play.filename, Action.screenshot):
            if settings_dict["quitbeforebossfight"] == True and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                time.sleep(1)
                travelEnd = quitBounty()
                break

            find_ellement(Button.play.filename, Action.move_and_click)

            time.sleep(0.5)
            retour = (
                selectCardsInHand()
            )  # Start the battle : the bot choose the cards and fight against the enemy
            log.info(f"goToEncounter - retour = {retour}")
            time.sleep(1)
            if retour == "win":
                log.info("goToEncounter : battle won")
                while True:
                    if not find_ellement(
                        UIElement.take_grey.filename, Action.screenshot
                    ):
                        mouse_click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if not find_ellement(
                        UIElement.replace_grey.filename, Action.screenshot
                    ):
                        mouse_click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if find_ellement(
                        UIElement.reward_chest.filename, Action.screenshot
                    ):
                        log.info(
                            "goToEncounter : " "Boss defeated. Time for REWARDS !!!"
                        )
                        collect()
                        travelEnd = True
                        break
            elif retour == "loose":
                travelEnd = True
                log.info("goToEncounter : Battle lost")
            else:
                travelEnd = True
                log.info("goToEncounter : don't know what happened !")

#            waitForItOrPass(UIElement.campfire, 5)
#            look_at_campfire_completed_tasks()
                
        else:
            if not nextlvl():
                break

    while not find_ellement(Button.back.filename, Action.screenshot):
        mouse_click()
        time.sleep(1)


def travelToLevel(page="next"):
    """
    Go to a Travel Point, choose a level/bounty and go on the road to make encounter
    """

    retour = False

    if find_ellement(
        f"levels/{settings_dict['location']}"
        f"_{settings_dict['mode']}_{settings_dict['level']}.png",
        Action.move_and_click,
        jthreshold["levels"],
    ):
        waitForItOrPass(Button.choose_level, 6)
        find_ellement(Button.choose_level.filename, Action.move_and_click)
        retour = True
    elif page == "next":
        if find_ellement(Button.sec.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("next")
        if retour is False and find_ellement(
            Button.fir.filename, Action.move_and_click
        ):
            time.sleep(1)
            retour = travelToLevel("previous")
        elif retour is False:
            find_ellement(Button.back.filename, Action.move_and_click)
    elif page == "previous":
        if find_ellement(Button.fir.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("previous")
        else:
            find_ellement(Button.back.filename, Action.move_and_click)
    return retour
