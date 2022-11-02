import sys
import random
import time
import json
import pathlib

from .platforms import windowMP
from .mouse_utils import (
    move_mouse_and_click,
    move_mouse,
    mouse_position,
    mouse_click,
    mouse_range,
)

from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .game import waitForItOrPass, defaultCase
from .encounter import selectCardsInHand
from .campfire import look_at_campfire_completed_tasks
from .log_board import LogHSMercs
from .settings import settings_dict, jthreshold
from .treasure import chooseTreasure
from .notification import send_notification, send_slack_notification

import logging

log = logging.getLogger(__name__)


def collect():
    """Collect the rewards just after beating the final boss of this level"""

    # it's difficult to find every boxes with lib CV2 so,
    # we try to detect just one and then we click on all known positions
    collectAttempts = 0

    while True:
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 3.5)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.5, windowMP()[3] / 2.4)
        move_mouse_and_click(windowMP(), windowMP()[2] / 2.7, windowMP()[3] / 1.4)

        move_mouse_and_click(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2.7)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.4, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.6, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.7, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.8, windowMP()[3] / 1.3)
        move_mouse_and_click(windowMP(), windowMP()[2] / 1.9, windowMP()[3] / 1.3)
        time.sleep(3)
        # if find_ellement(Button.done_bonus.filename, Action.move_and_click):
        #    time.sleep(5)
        #    continue
        collectAttempts += 1
        if find_ellement(Button.done.filename, Action.move_and_click):
            time.sleep(2)
            log.info("Clicking again if done button was not clicked before.")
            find_ellement(Button.done.filename, Action.move_and_click)
            break
        if collectAttempts > 10:
            send_notification(
                {
                    "message": f"Attempted to collect treasure {collectAttempts} times, attempting to recover."
                }
            )
            send_slack_notification(
                json.dumps(
                    {
                        "text": f"@channel Attempted to collect treasure {collectAttempts} times, attempting to recover."
                    }
                )
            )
            log.info(
                f"Attempted to collect treasure {collectAttempts} times, attempting to recover."
            )
            break

    # move the mouse to avoid a bug where the it is over a card/hero (at the end)
    # hiding the "OK" button
    move_mouse(windowMP(), windowMP()[2] // 1.25, windowMP()[3] // 1.25)
    # quit the bounty
    while not find_ellement(Button.finishok.filename, Action.move_and_click):
        time.sleep(1)
        mouse_click()
        time.sleep(2)


def quitBounty():
    """Function to (auto)quit the bounty. Called if the user configured it."""
    end = False
    if find_ellement(Button.view_party.filename, Action.move_and_click):
        while not find_ellement(UIElement.your_party.filename, Action.move):
            time.sleep(0.5)
        while not find_ellement(Button.retire.filename, Action.move_and_click):
            time.sleep(0.5)
        while not find_ellement(Button.lockin.filename, Action.move_and_click):
            time.sleep(0.5)
        end = True
        log.info("Quitting the bounty level before boss battle.")
    return end


def nextlvl():
    """Progress on the map (Boon, Portal, ...) to find the next battle"""
    time.sleep(3)
    retour = True

    if not find_ellement(Button.play.filename, Action.screenshot):

        if (
            find_ellement(UIElement.task_completed.filename, Action.screenshot)
            or find_ellement(UIElement.task_event_completed.filename, Action.screenshot)
            or find_ellement(
                UIElement.task_expansion_completed.filename, Action.screenshot
            )
        ):
            waitForItOrPass(UIElement.campfire, 10)
            look_at_campfire_completed_tasks()

        elif find_ellement(Button.reveal.filename, Action.move_and_click):
            time.sleep(1)
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] // 1.25)
            time.sleep(1.5)

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

        elif find_ellement(UIElement.campfire.filename, Action.screenshot):
            look_at_campfire_completed_tasks()
            time.sleep(3)

        # we add this test because, maybe we are not on "Encounter Map" anymore
        # (like after the final boss)
        elif find_ellement(UIElement.view_party.filename, Action.screenshot):
            search_battle_list = []
            battletypes = ["fighter", "protector", "caster"]
            random.shuffle(battletypes)
            battletypes.append("elite")
            for battletype in battletypes:
                tag = f"{battletype}_battle"
                coords = find_ellement(
                    getattr(UIElement, tag).filename, Action.get_coords
                )
                if coords:
                    battlepreference = f"prefer{battletype}"
                    x = coords[0]
                    y = coords[1] + (windowMP()[3] // 10.8)
                    if settings_dict[battlepreference]:
                        search_battle_list.insert(0, (x, y))
                    else:
                        search_battle_list.append((x, y))
            if search_battle_list:
                x, y = search_battle_list.pop(0)
                move_mouse_and_click(windowMP(), x, y)
                time.sleep(2)
            else:
                searchForEncounter()

        else:
            defaultCase()

    return retour


def searchForEncounter():
    retour = True
    if find_ellement(UIElement.view_party.filename, Action.screenshot):
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
        else:
            y = windowMP()[3] // 2.2
            log.debug(f"move mouse to (x, y) : ({x}, {y})")
            move_mouse_and_click(windowMP(), x, y)
    return retour


def goToEncounter():
    """
    Start new fight,
    continue on the road and collect everything (treasure, rewards, ...)
    """
    log.info("goToEncounter : entering")
    time.sleep(2)
    travelEnd = False

    while not travelEnd:

        if find_ellement(Button.play.filename, Action.screenshot):
            if settings_dict["stopatbossfight"] is True and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                send_notification({"message": "Stopping before Boss battle."})
                send_slack_notification(
                    json.dumps({"text": "@channel Stopping before Boss battle."})
                )
                log.info("Stopping before Boss battle.")
                sys.exit()

            if settings_dict["quitbeforebossfight"] is True and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                time.sleep(1)
                travelEnd = quitBounty()
                break

            # fix the problem with Hearthstone showing campfire just
            # after clicking on Play button
            while find_ellement(Button.play.filename, Action.move_and_click):
                time.sleep(1)
            # waitForItOrPass(UIElement.campfire, 3)
            # if look_at_campfire_completed_tasks():
            #    break

            zL = LogHSMercs(settings_dict["zonelog"])
            zL.start()
            retour = selectCardsInHand(
                zL
            )  # Start the battle : the bot choose the cards and fight against the enemy
            zL.stop()
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
                        send_notification(
                            {"message": "Boss defeated. Time for REWARDS !!!"}
                        )
                        send_slack_notification(
                            json.dumps({"text": "Boss defeated. Time for REWARDS !!!"})
                        )
                        log.info(
                            "goToEncounter : " "Boss defeated. Time for REWARDS !!!"
                        )
                        collect()
                        travelEnd = True
                        break
            elif retour == "loose":
                travelEnd = True
                send_notification({"message": "goToEncounter : Battle lost"})
                send_slack_notification(
                    json.dumps({"text": "goToEncounter : Battle lost"})
                )
                log.info("goToEncounter : Battle lost")
            else:
                travelEnd = True
                log.info("goToEncounter : don't know what happened !")

        else:
            if not nextlvl():
                break

    while not find_ellement(UIElement.bounties.filename, Action.screenshot):
        look_at_campfire_completed_tasks()
        move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.25)
        time.sleep(2)


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
        send_slack_notification(
            json.dumps({"text": f"Starting {settings_dict['location']} bounty."})
        )
        retour = True
    elif page == "next":
        if find_ellement(Button.arrow_next.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("next")
        if retour is False and find_ellement(
            Button.arrow_prev.filename, Action.move_and_click
        ):
            time.sleep(1)
            retour = travelToLevel("previous")
        elif retour is False:
            find_ellement(Button.back.filename, Action.move_and_click)
    elif page == "previous":
        if find_ellement(Button.arrow_prev.filename, Action.move_and_click):
            time.sleep(1)
            retour = travelToLevel("previous")
        else:
            find_ellement(Button.back.filename, Action.move_and_click)
    return retour


def selectGroup():
    """Look for the mercenaries group 'Botwork' and select it
    (click on 'LockIn' if necessary)"""

    log.debug("selectGroup : entering")

    # bad code but easily works
    # need to change it later to have a better solution
    group_name_custom = pathlib.PurePath(
        settings_dict["user_files_dir"],
        settings_dict["resolution"],
        Button.group_name.filename,
    ).as_posix()

    group_name = (
        f"../../{group_name_custom}"
        if pathlib.Path(group_name_custom).exists()
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
