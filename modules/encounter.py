import re
import time
import random
import configparser
import logging

from .platform import windowMP
from .mouse_utils import move_mouse_and_click, move_mouse, mouse_click, mouse_scroll

from .image_utils import partscreen, find_ellement
from .constants import UIElement, Checker, Button, Action
from .log_board import LogHSMercs
from .settings import settings_dict, mercslist, mercsAbilities, ability_order


log = logging.getLogger(__name__)


def select_enemy_to_attack(index):
    """Used to move the mouse over an enemy to attack it (after selecting a merc's ability)"""
    cardWidth = windowMP()[2] // 16
    cardHeight = windowMP()[3] // 6
    retour = False
    # find_element: Can be changed to return None or bool type
    if index:
        time.sleep(0.1)
        log.debug(
            f"Move index (index, x, y) : {index}"
            f" {index[0] + (cardWidth // 2)} {index[1] - (cardWidth // 3)}",
        )
        move_mouse_and_click(
            windowMP(), index[0] + (cardWidth // 3), index[1] - (cardHeight // 2)
        )
        retour = True

    return retour


def select_random_enemy_to_attack(enemies=[]):
    """look for a random enemy
    (used when blue mercs can't find red enemy,
    green can't find blue or
    red can't find green
    """
    log.debug("select_random_enemy_to_attack : attack random enemy")
    #    count = 0
    log.debug(f"{enemies} len={len(enemies)}")
    while enemies:
        toAttack = enemies.pop(random.randint(0, len(enemies) - 1))
        if select_enemy_to_attack(toAttack):
            break

    # right click added to avoid a problem when the bot detects no enemy
    # (it can't select another ability and we can hope an AoE will selected at least)
    # Update : add code to click in the middle of the enemy board
    #   when no enemy is detected
    mouse_click("right")


def select_ability(localhero):
    """Select an ability for a mercenary.
        Depend on what is available and wich Round (battle)
    Click only on the ability (doesnt move to an enemy)
    """
    global raund
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
    retour = False

    if localhero in mercsAbilities:
        if "Mercenary" in ability_order and localhero in ability_order["Mercenary"]:
            round_abilities = ability_order["Mercenary"][localhero].split(",")
            abilitiesNumber = len(round_abilities)
            if abilitiesNumber != 0:
                ability = raund % abilitiesNumber
                if ability == 0:
                    ability = int(round_abilities[len(round_abilities) - 1])
                else:
                    ability = int(round_abilities[ability - 1])
            else:
                ability = 1
        else:
            ability = 1

        chooseone3 = [windowMP()[2] // 3, windowMP()[2] // 2, windowMP()[2] // 1.5]
        log.info(f"ability selected : {ability}")
        if ability == 0:
            log.debug("No ability selected (0)")
            retour = False
        elif ability >= 1 and ability <= 3:
            log.debug(
                f"abilities Y : {abilitiesPositionY} |"
                f" abilities X : {abilitiesPositionX}"
            )
            partscreen(
                int(abilitiesWidth),
                int(abilitiesHeigth),
                int(windowMP()[1] + abilitiesPositionY),
                int(windowMP()[0] + abilitiesPositionX[0]),
            )
            # find_element: Can be changed to return None or bool type
            if (
                find_ellement(Checker.hourglass.filename, Action.get_coords_part_screen)
                is None
            ):
                move_mouse_and_click(
                    windowMP(),
                    int(abilitiesPositionX[ability - 1] + abilitiesWidth // 2),
                    int(abilitiesPositionY + abilitiesHeigth // 2),
                )
                if isinstance(mercsAbilities[localhero][str(ability)], bool):
                    retour = mercsAbilities[localhero][str(ability)]
                elif mercsAbilities[localhero][str(ability)] == "chooseone3":
                    time.sleep(0.2)
                    move_mouse_and_click(windowMP(), chooseone3[0], windowMP()[3] // 2)
                    retour = False
        else:
            log.info(f"No ability selected for {localhero}")
    else:
        localhero = re.sub(r" [0-9]$", "", localhero)
        if "Neutral" in ability_order and localhero in ability_order["Neutral"]:
            round_abilities = ability_order["Neutral"][localhero].split(",")
            abilitiesNumber = len(round_abilities)
            if abilitiesNumber != 0:
                ability = raund % abilitiesNumber
                if ability == 0:
                    ability = len(round_abilities)
                ability = int(round_abilities[ability - 1])
            else:
                ability = 1

            log.info(f"ability selected : {ability}")
            partscreen(
                int(abilitiesWidth),
                int(abilitiesHeigth),
                int(windowMP()[1] + abilitiesPositionY),
                int(windowMP()[0] + abilitiesPositionX[0]),
            )
            # find_element: Can be changed to return None or bool type
            if (
                find_ellement(Checker.hourglass.filename, Action.get_coords_part_screen)
                is None
            ):
                move_mouse_and_click(
                    windowMP(),
                    int(abilitiesPositionX[ability - 1] + abilitiesWidth // 2),
                    int(abilitiesPositionY + abilitiesHeigth // 2),
                )

                retour = True

    return retour


def attacks(
    position,
    mercName,
    number,
    enemyred,
    enemygreen,
    enemyblue,
    enemynoclass,
    enemynoclass2,
    mol,
):
    """Function to attack an enemy (red, green or blue ideally) with the selected mercenary
    red attacks green (if exists)
    green attacks blue (if exists)
    blue attacks red (if exists)
    else merc attacks minion with special abilities or neutral
    """
    global raund

    log.debug("Attacks function")

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
    y = windowMP()[3] / 1.5

    log.info(f"attack with : {mercName} ( position : {position}/{number} ={x})")

    move_mouse_and_click(windowMP(), x, y)
    time.sleep(0.2)
    move_mouse(windowMP(), windowMP()[2] / 3, windowMP()[3] / 2)
    if mercName in mercslist:
        if (
            mercslist[mercName]["type"] == "Protector"
            and select_ability(mercName)
            and not select_enemy_to_attack(enemygreen)
            and not select_enemy_to_attack(mol)
            and not select_enemy_to_attack(enemynoclass)
            and not select_enemy_to_attack(enemynoclass2)
        ):
            select_random_enemy_to_attack([enemyred, enemyblue])
        elif (
            mercslist[mercName]["type"] == "Fighter"
            and select_ability(mercName)
            and not select_enemy_to_attack(enemyblue)
            and not select_enemy_to_attack(mol)
            and not select_enemy_to_attack(enemynoclass)
            and not select_enemy_to_attack(enemynoclass2)
        ):
            select_random_enemy_to_attack([enemyred, enemygreen])
        elif (
            mercslist[mercName]["type"] == "Caster"
            and select_ability(mercName)
            and not select_enemy_to_attack(enemyred)
            and not select_enemy_to_attack(mol)
            and not select_enemy_to_attack(enemynoclass)
            and not select_enemy_to_attack(enemynoclass2)
        ):
            select_random_enemy_to_attack([enemygreen, enemyblue])
    elif select_ability(mercName):
        select_random_enemy_to_attack(
            [enemyred, enemygreen, enemyblue, enemynoclass, enemynoclass2]
        )


# Look for enemies
def find_enemies():
    enemyred = find_red_enemy()
    enemygreen = find_green_enemy()
    enemyblue = find_blue_enemy()
    enemynoclass = find_noclass_enemy()
    enemynoclass2 = find_noclass2_enemy()
    enemymol = find_mol_enemy()

    log.info(
        f"Enemies : red {enemyred}"
        f" - green {enemygreen}"
        f" - blue {enemyblue}"
        f" - noclass {enemynoclass}"
        f" - noclass2 {enemynoclass2}"
        f" - mol {enemymol}"
    )
    return enemyred, enemygreen, enemyblue, enemynoclass, enemynoclass2, enemymol


def find_red_enemy():
    return find_enemy("red")


def find_green_enemy():
    return find_enemy("green")


def find_blue_enemy():
    return find_enemy("blue")


def find_noclass_enemy():
    return find_enemy("noclass")


def find_noclass2_enemy():
    return find_enemy("noclass2")


def find_mol_enemy():
    return find_enemy("sob")


def find_enemy(enemy_type):
    enemy = find_ellement(
        getattr(UIElement, enemy_type).filename, Action.get_coords_part_screen
    )
    # find_element: Can be changed to return None or actual coords if exists
    if enemy:
        enemy = (
            enemy[0] + windowMP()[0],
            enemy[1] + windowMP()[1],
        )
    return enemy


def battle():
    """Find the cards on the battlefield (yours and those of your opponents)
    and make them battle until one of yours die
    """
    global raund
    retour = True

    # init the reading of Hearthstone filelog to detect your board / mercenaries
    zoneLog = LogHSMercs(settings_dict["zonelog"])
    zoneLog.start()

    raund = 1
    while True:
        move_mouse(
            windowMP(),
            windowMP()[2] // 2.6,
            windowMP()[3] // 1.09,
        )

        # we look for the (green) "ready" button because :
        # - sometimes, the bot click on it but it doesn't work very well
        # - during a battle, some enemies can return in hand and
        #   are put back on battlefield with a "ready" button
        #       but the bot is waiting for a victory / defeat /
        #   ... or the yellow button ready
        find_ellement(Button.allready.filename, Action.move_and_click)

        find_ellement(Button.onedie.filename, Action.move_and_click)

        if find_ellement(Checker.win.filename, Action.screenshot) or find_ellement(
            Checker.win_final.filename, Action.screenshot
        ):
            retour = "win"
            move_mouse_and_click(windowMP(), windowMP()[2] / 2, windowMP()[3] / 1.3)
            zoneLog.cleanBoard()

            break
        elif find_ellement(Checker.lose.filename, Action.screenshot):
            retour = "loose"
            move_mouse_and_click(
                windowMP(),
                windowMP()[2] / 2,
                windowMP()[3] / 1.3,
            )
            zoneLog.cleanBoard()
            break
        elif find_ellement(
            Button.fight.filename, Action.screenshot
        ):  # or find_ellement(Button.startbattle1.filename, Action.screenshot):

            # wait 'WaitForEXP' (float) in minutes, to make the battle longer and
            # win more EXP (for the Hearthstone reward track)
            wait_for_exp = settings_dict["waitforexp"]
            log.info(f"WaitForEXP - wait (second(s)) : {wait_for_exp}")
            time.sleep(wait_for_exp)

            # looks for your Mercenaries on board thanks to log file
            mercenaries = zoneLog.getBoard()
            log.info(f"ROUND {raund} : your board {mercenaries}")

            # click on neutral zone to avoid problem with screenshot
            # when you're looking for red/green/blue enemies
            move_mouse_and_click(windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2)

            time.sleep(0.2)

            # tmp = int(windowMP()[3] / 2)
            partscreen(windowMP()[2], windowMP()[3] // 2, windowMP()[1], windowMP()[0])

            (
                enemyred,
                enemygreen,
                enemyblue,
                enemynoclass,
                enemynoclass2,
                mol,
            ) = find_enemies()

            # Go (mouse) to "central zone" and click on an empty space
            # move_mouse_and_click(windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2)
            # time.sleep(1)

            for i in mercenaries:
                # Go (mouse) to "central zone" and click on an empty space
                move_mouse_and_click(
                    windowMP(), windowMP()[2] // 2, windowMP()[3] // 1.2
                )

                attacks(
                    int(i),
                    mercenaries[i],
                    int(sorted(mercenaries)[-1]),
                    enemyred,
                    enemygreen,
                    enemyblue,
                    enemynoclass,
                    enemynoclass2,
                    mol,
                )
                # in rare case, the bot detects an enemy ("noclass" most of the times) outside of the battlezone.
                # the second click (to select the enemy), which is on an empty space, doesnt work.
                # next move : instead of selecting the next mercenaries (to choose an ability),
                # the mercenary is clicked on to be targeted (from previous abilitay). Need a "rightclick" to cancel this action
                mouse_click("right")
                time.sleep(0.1)

            i = 0
            while True:
                if find_ellement(Button.allready.filename, Action.move_and_click):
                    break
                if i > 10:
                    mouse_click("right")
                    find_ellement(Button.fight.filename, Action.move_and_click)
                    break
                time.sleep(0.2)
                i += 1
            time.sleep(3)
            raund += 1

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

    log.debug("[ SETH - START]")
    retour = True

    while not find_ellement(Button.num.filename, Action.move):
        time.sleep(2)

    log.debug(f"windowMP = {windowMP()}")
    x1 = windowMP()[2] // 2.6
    y1 = windowMP()[3] // 1.09
    x2 = windowMP()[2] // 10
    y2 = windowMP()[3] // 10

    while not find_ellement(Button.num.filename, Action.move_and_click):
        move_mouse(windowMP(), x1, y1)
        move_mouse(windowMP(), x2, y2)

    retour = battle()
    log.debug("[ SETH - END]")

    return retour
