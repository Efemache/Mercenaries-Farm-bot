import re
import time
import random
import configparser

import pyautogui


from .platform import windowMP
from .mouse_utils import mouse_random_movement, move_mouse_and_click, move_mouse
from .debug import debug
from .image_utils import partscreen, find_ellement
from .constants import UIElement, Checker, Button, Action
from .log_board import LogHSMercs
from .settings import settings


def move(index):
    """Used to move the mouse to an enemy (from a selected merc's ability)"""
    cardWidth = windowMP()[2] // 16
    cardHeight = windowMP()[3] // 6
    if index != (0, 0):
        time.sleep(0.1)
        pyautogui.moveTo(
            index[0] + (cardWidth // 3),
            index[1] - (cardHeight // 2),
            0.6,
            mouse_random_movement(),
        )
        debug(
            "Move index (index, x, y) : ",
            index,
            index[0] + (cardWidth // 2),
            index[1] - (cardWidth // 3),
        )
        time.sleep(0.1)
        pyautogui.click()
        return True
    else:
        return False


def rand(enemyred, enemygreen, enemyblue, enemynoclass):
    """look for a random enemy
    (used when blue mercs can't find red enemy,
    green can't find blue or
    red can't find green
    """
    debug("rand : attack random enemy")
    #    count = 0
    enemies = [enemyred, enemygreen, enemyblue, enemynoclass]
    debug(enemies, "len=", len(enemies))
    while enemies:
        toAttack = enemies.pop(random.randint(0, len(enemies) - 1))
        if move(toAttack):
            break

    # right click added to avoid a problem when the bot detects no enemy
    # (it can't select another ability and we can hope an AoE will selected at least)
    # Update : add code to click in the middle of the enemy board
    #   when no enemy is detected
    pyautogui.rightClick()


def abilities(localhero):
    """Select an ability for a mercenary.
        Depend on what is available and wich Round (battle)
    Click only on the ability (doesnt move to an enemy)
    """
    global mercsAbilities
    abilitiesWidth = windowMP()[2] // 14.2
    abilitiesHeigth = windowMP()[3] // 7.2

    # abilitiesPositionY : Y coordinate to find "abilities" line during battle
    abilitiesPositionY = windowMP()[3] // 2.4
    # abilitiesPositionX :
    #   X coordinates to find the 3 "abilities" during battle
    #   (4 because sometimes, Treasure give you a new abilities
    #   but the bot doesn't support it right now)
    abilitiesPositionX = [
        windowMP()[2] // 2.68,
        windowMP()[2] // 2.17,
        windowMP()[2] // 1.8,
        windowMP()[2] // 1.56,
    ]
    # mercsAbilities=readjson('conf/attacks.json')
    retour = False

    config = configparser.ConfigParser()
    config.read("conf/combo.ini")
    if localhero in mercsAbilities:
        if config.has_option("Mercenary", localhero):
            round_abilities = config["Mercenary"][localhero].split(",")
            abilitiesNumber = len(round_abilities)
            if abilitiesNumber != 0:
                ability = raund % abilitiesNumber
                if ability == 0:
                    ability = int(round_abilities[len(round_abilities) - 1])
                elif round_abilities[ability - 1] != "-":
                    ability = int(round_abilities[ability - 1])
                else:
                    ability = "-"
            else:
                ability = 1
        else:
            ability = 1

        # chooseone3=[640, 960, 1280]
        chooseone3 = [windowMP()[2] // 3, windowMP()[2] // 2, windowMP()[2] // 1.5]
        print(f"ability selected : {ability}")
        if ability == "-":
            debug("No ability selected (-)")
            retour = False
        elif ability >= 1 and ability <= 3:
            debug(
                f"abilities Y : {abilitiesPositionY} |"
                f" abilities X : {abilitiesPositionX}"
            )
            partscreen(
                int(abilitiesWidth),
                int(abilitiesHeigth),
                int(windowMP()[1] + abilitiesPositionY),
                int(windowMP()[0] + abilitiesPositionX[0]),
            )
            if find_ellement(
                Checker.hourglass.filename, Action.get_coords_part_screen
            ) == (
                0,
                0,
            ):  # Checker.hourglass : hourglass
                pyautogui.moveTo(
                    int(
                        windowMP()[0]
                        + abilitiesPositionX[ability - 1]
                        + abilitiesWidth // 2
                    ),
                    int(windowMP()[1] + abilitiesPositionY + abilitiesHeigth // 2),
                    settings["MouseSpeed"],
                    mouse_random_movement(),
                )
                pyautogui.click()
                if isinstance(mercsAbilities[localhero][str(ability)], bool):
                    retour = mercsAbilities[localhero][str(ability)]
                elif mercsAbilities[localhero][str(ability)] == "chooseone3":
                    time.sleep(0.2)
                    move_mouse_and_click(windowMP(), chooseone3[0], windowMP()[3] // 2)
                    retour = False
        else:
            print(f"No ability selected for {localhero}")
    else:
        localhero = re.sub(r" [0-9]$", "", localhero)
        if config.has_option("Neutral", localhero):
            round_abilities = config["Neutral"][localhero].split(",")
            abilitiesNumber = len(round_abilities)
            if abilitiesNumber != 0:
                ability = raund % abilitiesNumber
                if ability == 0:
                    ability = len(round_abilities)
                ability = int(round_abilities[ability - 1])
            else:
                ability = 1

            print(f"ability selected : {ability}")
            partscreen(
                int(abilitiesWidth),
                int(abilitiesHeigth),
                int(windowMP()[1] + abilitiesPositionY),
                int(windowMP()[0] + abilitiesPositionX[0]),
            )
            if find_ellement(
                Checker.hourglass.filename, Action.get_coords_part_screen
            ) == (
                0,
                0,
            ):
                move_mouse_and_click(
                    windowMP(),
                    int(abilitiesPositionX[ability - 1] + abilitiesWidth // 2),
                    int(abilitiesPositionY + abilitiesHeigth // 2),
                )

                retour = True

    return retour


def attacks(
    position, mercName, number, enemyred, enemygreen, enemyblue, enemynoclass, mol
):
    """Function to attack an enemy (red, green or blue ideally) with the selected mercenary
    red attacks green (if exists)
    green attacks blue (if exists)
    blue attacks red (if exists)
    else merc attacks minion with special abilities or neutral
    """
    global mercslist

    debug("[DEBUG] Attacks function")

    cardSize = int(windowMP()[2] / 12)
    firstOdd = int(windowMP()[0] + (windowMP()[2] / 3))
    firstEven = int(windowMP()[0] + (windowMP()[2] / 3.6))

    # positionEven=[560,720,880,1040,1200,1360]
    # positionOdd=[640,800,960,1120,1280]
    positionOdd = []
    positionEven = []
    for i in range(6):
        positionEven.append(int(firstEven + (i * cardSize)))
        if i != 5:
            positionOdd.append(int(firstOdd + (i * cardSize)))

    if number % 2 == 0:  # if mercenaries number is even
        pos = int(2 - (number / 2 - 1) + (position - 1))
        x = positionEven[pos]
    else:  # if mercenaries number is odd
        pos = int(2 - (number - 1) / 2 + (position - 1))
        x = positionOdd[pos]
    y = windowMP()[1] + windowMP()[3] / 1.5

    print(
        "attack with : ", mercName, "( position :", position, "/", number, "=", x, ")"
    )

    # print("merclist", mercslist.keys())
    pyautogui.moveTo(x, y, settings["MouseSpeed"], mouse_random_movement())
    pyautogui.click()
    time.sleep(0.2)
    move_mouse(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2)
    if mercName in mercslist:
        if (
            mercslist[mercName]["type"] == "Protector"
            and abilities(mercName)
            and not move(enemygreen)
            and not move(mol)
            and not move(enemynoclass)
        ):
            rand(enemyred, enemygreen, enemyblue, enemynoclass)
        elif (
            mercslist[mercName]["type"] == "Fighter"
            and abilities(mercName)
            and not move(enemyblue)
            and not move(mol)
            and not move(enemynoclass)
        ):
            rand(enemyred, enemygreen, enemyblue, enemynoclass)
        elif (
            mercslist[mercName]["type"] == "Caster"
            and abilities(mercName)
            and not move(enemyred)
            and not move(mol)
            and not move(enemynoclass)
        ):
            rand(enemyred, enemygreen, enemyblue, enemynoclass)
    elif abilities(mercName):
        rand(enemyred, enemygreen, enemyblue, enemynoclass)


def battle():
    """Find the cards on the battlefield (yours and those of your opponents)
    and make them battle until one of yours die
    """
    global raund
    #    global threshold
    global speed
    global zoneLog
    retour = True

    # init the reading of Hearthstone filelog to detect your board / mercenaries
    zoneLog = LogHSMercs(settings["Zonelog"])
    zoneLog.start()

    #    tempthreshold = threshold
    raund = 1
    while True:
        pyautogui.moveTo(
            windowMP()[0] + (windowMP()[2] / 2.6),
            windowMP()[1] + (windowMP()[3] * 0.92),
            settings["MouseSpeed"],
            mouse_random_movement(),
        )
        speed = 0
        #        threshold = 0.85

        # we look for the (green) "ready" button because :
        # - sometimes, the bot click on it but it doesn't work very well
        # - during a battle, some enemies can return in hand and
        #   are put back on battlefield with a "ready" button
        #       but the bot is waiting for a victory / defeat /
        #   ... or the yellow button ready
        find_ellement(
            Button.allready.filename, Action.move_and_click
        )  # buttons 14: 'allready'

        find_ellement(
            Button.onedie.filename, Action.move_and_click
        )  # buttons 20: 'onedie'

        if find_ellement(Checker.win.filename, Action.screenshot):  # chekers 13: 'win'
            retour = "win"
            move_mouse_and_click(
                windowMP(), windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.6
            )
            zoneLog.cleanBoard()

            break
        elif find_ellement(Checker.lose.filename, Action.screenshot):
            retour = "loose"
            move_mouse_and_click(
                windowMP(),
                windowMP()[2] / 2,
                windowMP()[3] - windowMP()[3] / 4.6,
            )
            zoneLog.cleanBoard()
            break
        elif find_ellement(
            Button.fight.filename, Action.screenshot
        ):  # or find_ellement(Button.startbattle1.filename, Action.screenshot):
            # wait 'WaitForEXP' (float) in minutes, to make the battle longer and
            # win more EXP (for the Hearthstone reward track)
            print("WaitForEXP - wait (second(s)) :", settings["WaitForEXP"])
            time.sleep(settings["WaitForEXP"])

            # looks for your Mercenaries on board thanks to log file
            mercenaries = zoneLog.getBoard()
            print("ROUND", raund, " : your board", mercenaries)

            # click on neutral zone to avoid problem with screenshot
            # when you're looking for red/green/blue enemies
            move_mouse_and_click(
                windowMP(), windowMP()[2] / 2, windowMP()[3] - windowMP()[3] / 4.6
            )

            time.sleep(0.2)

            # tmp = int(windowMP()[3] / 2)
            partscreen(windowMP()[2], windowMP()[3] // 2, windowMP()[1], windowMP()[0])

            temp = speed
            # threshold = 0.8

            # Look for enemies
            enemyred = find_ellement(
                UIElement.red.filename, Action.get_coords_part_screen
            )
            if enemyred != (0, 0):
                enemyred = (enemyred[0] + windowMP()[0], enemyred[1] + windowMP()[1])

            enemygreen = find_ellement(
                UIElement.green.filename, Action.get_coords_part_screen
            )
            if enemygreen != (0, 0):
                enemygreen = (
                    enemygreen[0] + windowMP()[0],
                    enemygreen[1] + windowMP()[1],
                )

            enemyblue = find_ellement(
                UIElement.blue.filename, Action.get_coords_part_screen
            )
            if enemyblue != (0, 0):
                enemyblue = (enemyblue[0] + windowMP()[0], enemyblue[1] + windowMP()[1])

            enemynoclass = find_ellement(
                UIElement.noclass.filename, Action.get_coords_part_screen
            )
            if enemynoclass != (0, 0):
                enemynoclass = (
                    enemynoclass[0] + windowMP()[0],
                    enemynoclass[1] + windowMP()[1],
                )

            mol = find_ellement(UIElement.sob.filename, Action.get_coords_part_screen)
            if mol != (0, 0):
                mol = (mol[0] + windowMP()[0], mol[1] + windowMP()[1])
            print(
                "Enemies : red",
                enemyred,
                " - green",
                enemygreen,
                " - blue",
                enemyblue,
                " - noclass",
                enemynoclass,
                " - mol",
                mol,
            )

            # Go (mouse) to "central zone" and click on an empty space
            pyautogui.moveTo(
                windowMP()[0] + windowMP()[2] / 2,
                windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8,
                settings["MouseSpeed"],
                mouse_random_movement(),
            )
            pyautogui.click()
            time.sleep(1)

            for i in mercenaries:
                # Go (mouse) to "central zone" and click on an empty space
                pyautogui.moveTo(
                    windowMP()[0] + windowMP()[2] / 2,
                    windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8,
                    settings["MouseSpeed"],
                    mouse_random_movement(),
                )
                pyautogui.click()

                attacks(
                    int(i),
                    mercenaries[i],
                    int(sorted(mercenaries)[-1]),
                    enemyred,
                    enemygreen,
                    enemyblue,
                    enemynoclass,
                    mol,
                )
                time.sleep(0.1)

            # threshold = 0.75
            speed = temp
            i = 0
            while True:
                if find_ellement(
                    Button.allready.filename, Action.move_and_click
                ):  # buttons 14: 'allready'
                    break
                if i > 10:
                    pyautogui.rightClick()
                    find_ellement(
                        Button.fight.filename, Action.move_and_click
                    )  # buttons 15: 'fight'
                    break
                time.sleep(0.2)
                i += 1
            time.sleep(3)
            raund += 1
    # threshold = tempthreshold
    zoneLog.stop()
    return retour


def selectCardsInHand():
    """Select the cards to put on battlefield
    and then, start the 'battle' function
    Update : actually, the bot doesn't choose it anymore
    since we stopped to use image with mercenaries text
    (so we can easily support multi-language)
        this feature will come back later using HS logs
    """

    debug("[ SETH - START]")
    retour = True

    global speed
    #    global threshold

    while not find_ellement(Button.num.filename, Action.move):  # buttons 5: 'num'
        time.sleep(0.5)

    debug("windowsMP() : ", windowMP())
    x = windowMP()[0] + (windowMP()[2] / 2.6)
    y = windowMP()[1] + (windowMP()[3] * 0.92)
    speed = 0
    # threshold = 0.85

    while not find_ellement(
        Button.num.filename, Action.move_and_click
    ):  # buttons 5: 'num'
        pyautogui.moveTo(x, y, settings["MouseSpeed"])
        # time.sleep(1)
        pyautogui.moveTo(
            windowMP()[0] + (windowMP()[2] * 0.1),
            windowMP()[1] + (windowMP()[3] * 0.1),
            settings["MouseSpeed"],
            mouse_random_movement(),
        )

    retour = battle()
    debug("[ SETH - END]")

    return retour
