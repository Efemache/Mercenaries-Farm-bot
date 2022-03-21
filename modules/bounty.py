import random
import time

import pyautogui


from .platform import windowMP
from .mouse_utils import mouse_random_movement, move_mouse_and_click, move_mouse
from .debug import debug
from .constants import UIElement, Button, Action
from .image_utils import find_ellement
from .settings import settings
from .game import waitForItOrPass
from .encounter import selectCardsInHand


def collect():
    """Collect the rewards just after beating the final boss of this level"""
    #    global threshold
    #    tmpthreshold = threshold
    #    threshold = 0.65
    #    threshold = 0.59

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
    #    threshold = tmpthreshold

    # move the mouse to avoid a bug where the it is over a card/hero (at the end)
    # masking the "OK" button
    move_mouse(windowMP(), windowMP()[2] * 0.8, windowMP()[3] * 0.8)
    # quit the bounty
    while not find_ellement(Button.finishok.filename, Action.move_and_click):
        time.sleep(1)
        pyautogui.click()
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

    if not find_ellement(Button.play.filename, Action.screenshot):

        if find_ellement(Button.reveal.filename, Action.move_and_click):
            time.sleep(1)
            move_mouse_and_click(
                windowMP(), windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.8
            )
            time.sleep(1.5)

        elif find_ellement(Button.visit.filename, Action.move_and_click):
            y = windowMP()[1] + windowMP()[3] / 2.2
            time.sleep(7)
            while find_ellement(UIElement.visitor.filename, Action.screenshot):
                temp = random.choice([3, 2, 1.7])
                x = windowMP()[2] // temp

                pyautogui.moveTo(x, y, settings["MouseSpeed"], mouse_random_movement())
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.2)
                find_ellement(Button.choose_task.filename, Action.move_and_click)
                time.sleep(0.2)
                pyautogui.click()
                time.sleep(8)

        elif find_ellement(
            UIElement.pick.filename, Action.move_and_click
        ) or find_ellement(Button.portal_warp.filename, Action.move_and_click):
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)
        elif find_ellement(UIElement.surprise.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.surprise.filename, Action.move_and_click)

        elif find_ellement(UIElement.spirithealer.filename, Action.screenshot):
            # type A
            time.sleep(1)
            find_ellement(UIElement.spirithealer.filename, Action.move_and_click)
        else:
            x, y = pyautogui.position()
            debug("Mouse (x, y) : ", x, y)
            if y == windowMP()[1] + windowMP()[3] // 2.2:
                x += windowMP()[2] // 25
                if x > windowMP()[0] + windowMP()[2]:
                    x = windowMP()[0] + windowMP()[2] / 3.7
            else:
                x = windowMP()[0] + windowMP()[2] // 3.7
                y = windowMP()[1] + windowMP()[3] // 2.2
            debug("move mouse to (x, y) : ", x, y)
            pyautogui.moveTo(x, y, settings["MouseSpeed"])
            time.sleep(0.1)
            pyautogui.doubleClick()


def chooseTreasure():
    """used to choose a Treasure after a battle/fight
    Note: should be updated to select "good" (passive?) treasure instead of a random one
    """
    y = windowMP()[3] / 2
    temp = random.randint(0, 2)
    if temp == 0:
        x = windowMP()[2] / 2.3
        pyautogui.moveTo(x, y, settings["MouseSpeed"], mouse_random_movement())
    if temp == 1:
        x = windowMP()[2] / 1.7
        pyautogui.moveTo(x, y, settings["MouseSpeed"], mouse_random_movement())
    if temp == 2:
        x = windowMP()[2] / 1.4
        pyautogui.moveTo(x, y, settings["MouseSpeed"], mouse_random_movement())
    pyautogui.click()
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
    #    global threshold
    #    tempthreshold = threshold
    #    threshold = 0.65

    if find_ellement(UIElement.travelpoint.filename, Action.screenshot):

        pyautogui.moveTo(
            windowMP()[0] + windowMP()[2] / 1.5,
            windowMP()[1] + windowMP()[3] / 2,
            settings["MouseSpeed"],
            mouse_random_movement(),
        )

        pyautogui.scroll(50)
        time.sleep(0.5)

        if settings["location"] == "The Barrens":
            find_ellement(UIElement.Barrens.filename, Action.move_and_click)

        elif settings["location"] == "Felwood":
            find_ellement(UIElement.Felwood.filename, Action.move_and_click)

        elif settings["location"] == "Winterspring":
            pyautogui.scroll(-2)
            pyautogui.moveTo(
                windowMP()[0] + windowMP()[2] / 3,
                windowMP()[1] + windowMP()[3] / 2,
                settings["MouseSpeed"],
                mouse_random_movement(),
            )
            time.sleep(0.5)
            find_ellement(UIElement.Winterspring.filename, Action.move_and_click)

        elif settings["location"] == "Blackrock":
            pyautogui.scroll(-10)
            pyautogui.moveTo(
                windowMP()[0] + windowMP()[2] / 3,
                windowMP()[1] + windowMP()[3] / 2,
                settings["MouseSpeed"],
                mouse_random_movement(),
            )
            time.sleep(0.5)
            find_ellement(UIElement.Blackrock.filename, Action.move_and_click)

        elif settings["location"] == "Alterac":
            pyautogui.scroll(-15)
            pyautogui.moveTo(
                windowMP()[0] + windowMP()[2] / 3,
                windowMP()[1] + windowMP()[3] / 2,
                settings["MouseSpeed"],
                mouse_random_movement(),
            )
            time.sleep(0.5)
            find_ellement(UIElement.Alterac.filename, Action.move_and_click)

        else:
            print(
                "[INFO] Travel Point unknown. "
                "The bot won't change the one already selected."
            )

        pyautogui.moveTo(
            windowMP()[0] + windowMP()[2] / 2,
            windowMP()[1] + windowMP()[3] / 2,
            settings["MouseSpeed"],
            mouse_random_movement(),
        )
        time.sleep(0.5)

        if settings["mode"] == "Normal":
            find_ellement(UIElement.normal.filename, Action.move_and_click)
        elif settings["mode"] == "Heroic":
            find_ellement(UIElement.heroic.filename, Action.move_and_click)
        else:
            print("[INFO] Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(Button.sta, 2)
    find_ellement(Button.sta.filename, Action.move_and_click)
    # threshold = tempthreshold


def goToEncounter():
    """
    Start new fight,
    continue on the road and collect everything (treasure, rewards, ...)
    """
    print("goToEncounter : entering")
    #    global threshold
    # global zoneLog
    time.sleep(2)
    travelEnd = False

    # zoneLog = LogHSMercs(settings["Zonelog"])
    # zoneLog.start()
    while not travelEnd:
        # tempthreshold = threshold
        # threshold = 0.85

        if find_ellement(Button.play.filename, Action.screenshot):
            if settings["quitBeforeBossFight"] == "True" and find_ellement(
                UIElement.boss.filename, Action.screenshot
            ):
                time.sleep(1)
                travelEnd = quitBounty()
                break

            find_ellement(Button.play.filename, Action.move_and_click)

            time.sleep(0.5)
            # threshold = tempthreshold
            retour = (
                selectCardsInHand()
            )  # Start the battle : the bot choose the cards and fight against the enemy
            print("goToEncounter - retour = ", retour)
            time.sleep(1)
            if retour == "win":
                print("goToEncounter : battle won")
                while True:
                    # ToDo : add a tempo when you detect a new completed task
                    # if find (task completed) :
                    #   time.sleep(2)

                    if not find_ellement(
                        UIElement.take_grey.filename, Action.screenshot
                    ):
                        pyautogui.click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if not find_ellement(
                        UIElement.replace_grey.filename, Action.screenshot
                    ):
                        pyautogui.click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if find_ellement(
                        UIElement.presents_thing.filename, Action.screenshot
                    ):
                        print(
                            "goToEncounter : "
                            "Wow! You beat the Boss. Time for REWARDS !!!"
                        )
                        collect()
                        travelEnd = True
                        break
            elif retour == "loose":
                travelEnd = True
                print("goToEncounter : Battle lost")
            else:
                travelEnd = True
                print("goToEncounter : don't know what happened !")
        else:
            # threshold = tempthreshold
            nextlvl()
    # threshold = tempthreshold
    # zoneLog.stop()
    while not find_ellement(Button.back.filename, Action.screenshot):
        pyautogui.click()
        time.sleep(1)


def travelToLevel(page="next"):
    """
    Go to a Travel Point, choose a level/bounty and go on the road to make encounter
    """

    retour = False

    if find_ellement(UIElement.bounties.filename, Action.screenshot):
        if find_ellement(
            "levels/"
            + settings["location"]
            + "_"
            + settings["mode"]
            + "_"
            + settings["level"]
            + ".png",
            Action.move_and_click,
            0.4,
        ):
            waitForItOrPass(Button.start, 6)
            find_ellement(Button.start.filename, Action.move_and_click)
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
