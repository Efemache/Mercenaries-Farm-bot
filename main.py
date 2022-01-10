#! /usr/bin/env python3
import time
import cv2
import numpy as np
from mss import mss
import mss
import configparser
import random
from tkinter import *
import threading
import keyboard
from tkinter.ttk import *
from PIL import Image
import os
import sys
import pyautogui
import json
from modules.log_board import *
 
## try to detect the OS (Windows, Linux, Mac, ...)
## to load specific libs
if sys.platform in ['Windows', 'win32', 'cygwin']:
    myOS = 'windows'
    try:
        from ahk import AHK
        ahk = AHK()
    except ImportError:
        print("ahk not installed")
elif sys.platform in ['linux', 'linux2']:
    myOS = 'linux'
    try:
        import gi
        gi.require_version("Wnck", "3.0")
        from gi.repository import Wnck, Gtk
    except ImportError:
        print("gi.repository not installed")
else:
    myOS = 'unknown'
    print("sys.platform='{platform}' is unknown.".format(platform=sys.platform))
    exit(1)


global screenImg
global partImg
global threshold
global jthreshold
global zoneLog
threshold = 0.75
global mercslist
mercslist={}

# Ui-ellements
Ui_Ellements = ['battle', 'blue', 'green', 'group', 'next', 'one', 'page_1', 'page_2', 'page_3', 'red', 'prev', 'sob',
                'noclass', 'bat1', 'bat2', 'bat3', 'bat4', 'bat5', 'take_grey', 'sombody', 'bounties',
                'bounties', 'Barrens', 'startbat', 'pick', 'Winterspring', 'Felwood', 'normal',
                'heroic','replace_grey', 'travelpoint','presents_thing', 'free_battle', 'choose_team', 'view_party']  # noclass 12, bat5-17
# buttons
buttons = ['back', 'continue', 'create', 'del', 'join_button', 'num', 'ok', 'play', 'ready', 'sec', 'sta', 'start',
           'start1', 'submit', 'allready', 'startbattle', 'startbattle1', 'take', 'choose_task', 'portal-warp', 'onedie', 'reveal',
           'done', 'finishok', 'confirm', 'visit','fir','replace', 'keep']  # last take -17
# chekers
chekers = ['30lvl', 'empty_check', 'find', 'goto', 'group_find', 'level_check', 'rename', 'shab', 'drop', '301', '302',
           'taken', 'text', 'win', 'ifrename', 'levelstarted', 'nextlvlcheck', 'cords-search', '303', '30lvl1',
           '30lvl2', 'menu', 'party','lose']

# Settings - 0: MonitorResolution (1920x1080), 1: level (20), 2: location (The Barrens), 3: mode (Heroic), 4: GroupCreate (True), 5: heroSet (True), 6: GameDir (path)
setings = []
## heroes
#hero = []
#hero_colour = []
#heroNUM = ['', '', '', '', '', '']
## for battle
#herobattle = []
#herobattlefin = []
# damp
enemywiz = [0, 0, 0, 0, 0, 0]
#heroTEMP = []
# img list
picparser = ['/1.png', '/2.png', '/3.png', '/4.png']

debug_mode=False
def debug(*message):
    if debug_mode :
        print("[DEBUG] ", message)

# window multi-platorms (Windows & Linux support)
def windowMP() :
    if(myOS=='windows'):
        retour=win.rect
    elif(myOS=='linux'):
        retour=win.get_client_window_geometry()
    else:
        retour=None
    return retour

# define function to use serveral mouse movements on Windows & Linux
def mouse_random_movement():
    return random.choices([pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad])[0]

def readjson(jfile) :
    descriptor = open(jfile)
    data = json.load(descriptor)
    descriptor.close()
    return data

def configread():
    """ Read settings.ini and put it in a table :
            Setings - 0: MonitorResolution (1920x1080), 1: level (20), 2: location (The Barrens), 3: mode (Heroic), 4: GroupCreate (True), 5: heroSet (True),
            6: monitor (1), 7: MouseSpeed (0.5), 8: WaitForEXP (3), 9: Zonelog (GameDir/Logs/Zone.log)
    """
    global jthreshold
    global mercslist

    global Resolution
    global speed

    config = configparser.ConfigParser()
    config.read("settings.ini")
    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])
    n = 0

    setings.append(config["BotSettings"]["Monitor Resolution"].replace('*', 'x'))
    for i in ["level", "location", "mode", "GroupCreate", "heroesSet"]:
        setings.append(config["BotSettings"][i])
    setings.append(int(config["BotSettings"]["monitor"]))
    setings.append(float(config["BotSettings"]["MouseSpeed"]))
    setings.append(float(config["BotSettings"]["WaitForEXP"])*60)
    if os.path.exists(config["BotSettings"]["GameDir"] + '/Hearthstone.exe') :
        setings.append(config["BotSettings"]["GameDir"] + '/Logs/Zone.log')
    else :
        print("[ERROR] Set the correct Hearthstone Game Directory in settings.ini ('GameDir' var)")
        # yeah it's bad coding but don't have time to change everything else
        exit(2)
        
    jthreshold = readjson("js/thresholds.json")
    mercslist = readjson("js/mercs.json")

    #print(setings)
#    files = os.listdir('./files/1920x1080/heroes')
#    for obj in files:
#        for i in range(6):
#            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
#            if rt != 'auto' and rt != '-':
#                if rt == obj.split(".")[0] or rt in obj.split(".")[1]:
#                    print(rt)
#                    hero.append(obj)
#                    hero_colour.append(obj.split(".")[2])
#    for n in range(2):
#        for i in range(6):
#            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
#            if rt == 'auto' and n==0:
#                print(rt)
#                hero.append(rt)
#                hero_colour.append(rt)
#            if rt == '-' and n==1:
#                print(rt)
#                hero.append(rt)
#                hero_colour.append(rt)
    
    print(setings)


def filepp(name, strname):
    try:
        i = 0
        while i < len(name):
            name[i] = strname + "/" + name[i] + ".png"
            i += 1
    except:
        print(strname, "file list got error")


def parslist():
    filepp(Ui_Ellements, "UI_ellements")
    filepp(buttons, "buttons")
    filepp(chekers, "chekers")
    i = 0
    #while i < len(hero):
    #    hero[i] = "heroes/" + hero[i]
    #    i += 1
    #return 0


def screen():
    global screenImg
    sct = mss.mss()
    if debug_mode :
        # setings 0: 'MonitorResolution(ex:1920x1080)'
        filename = sct.shot(mon=setings[6], output='files/' + setings[0] + '/screen.png')
    screenImg = np.array(sct.grab(sct.monitors[setings[6]]))


def partscreen(x, y, top, left):
    global partImg
    print("entered screenpart")
    import mss.tools
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": x, "height": y}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        if debug_mode :
            # setings 0: 'MonitorResolution(ex:1920x1080)'
            mss.tools.to_png(sct_img.rgb, sct_img.size, output='files/' + setings[0] + '/part.png')
        partImg = np.array(sct_img)

def findgame():
    global win
    retour = False

    try:
        if(myOS=='linux'):
            screenHW = Wnck.Screen.get_default()
            while Gtk.events_pending():
                Gtk.main_iteration()
            windows = screenHW.get_windows()

            for w in windows:
                if(w.get_name() == 'Hearthstone'):
                    win = w
                    win.activate(int(time.time()))
                    win.make_above()
                    retour = True
        elif(myOS=='windows'):
            win = ahk.win_get(title='Hearthstone')
            retour = True
        else:
            print("OS not supported.")
    except:
        print("No game found.")
    return retour


""" Used to move the mouse to an enmey (from a selected merc's ability)
"""
def move(index):
    if index != (0, 0):
        time.sleep(0.2)
        pyautogui.moveTo(index[0] + 40, index[1] - 30, 0.6, mouse_random_movement())
        debug("Move index (index, x, y) : ",index, index[0] + 40, index[1] - 30)
        time.sleep(0.1)
        pyautogui.click()
        return False
    else:
        return True


def rand(enemyred, enemygreen, enemyblue, enemynoclass):
    count = 0
    while True:
        a = random.randint(0, 2)
        if a == 0:
            if not move(enemygreen):
                break
            else:
                count += 1
        if a == 1:
            if not move(enemyred):
                break
            else:
                count += 1
        if a == 2:
            if not move(enemyblue):
                break
            else:
                count += 1
        if count > 5:
            # sometimes there is one central enemy but sometimes you have two enemies
            # in this case, there is no minion in the middle so you have to move the mouse to a position
            # which can touch one central minion or one on the left
            x = int(windowMP()[0] + (windowMP()[2] / 2) - (windowMP()[2] / 68))
            y = int(windowMP()[1] + (windowMP()[3] / 4))
            pyautogui.dragTo(x, y, 0.6, mouse_random_movement())
            time.sleep(0.1)
            pyautogui.click()
            break


def collect():
    """ Collect the rewards just after beating the final boss of this level
    """
    global threshold
    tmpthreshold = threshold
#    threshold = 0.65
    threshold = 0.59

    # it's difficult to find every boxes with lib CV2 so, we try to detect just one and then we click on all known positions
    while not find_ellement(buttons[22], 14) :	# buttons 22: 'done'
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2.5, windowMP()[1] + windowMP()[3] / 3.5, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] / 3.5, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 3.5, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2.4, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2.7, windowMP()[1] + windowMP()[3] / 1.4, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 3, windowMP()[1] + windowMP()[3] / 2.7, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.7, windowMP()[1] + windowMP()[3] / 1.3, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.6, windowMP()[1] + windowMP()[3] / 1.3, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.8, windowMP()[1] + windowMP()[3] / 1.3, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.9, windowMP()[1] + windowMP()[3] / 1.3, setings[7], mouse_random_movement())
        pyautogui.click()
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.4, windowMP()[1] + windowMP()[3] / 1.3, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(1)
    threshold = tmpthreshold

    # move the mouse to avoid a bug where the it is over a card/hero (at the end) masking the "OK" button
    pyautogui.moveTo(windowMP()[0] + windowMP()[2] * 0.8, windowMP()[1] + windowMP()[3] * 0.8, setings[7], mouse_random_movement())

    # quit the bounty
    while not find_ellement(buttons[23], 14):	# buttons 23: 'finishok'
        pyautogui.click()
        time.sleep(0.5)


def nextlvl():
    """ Progress on the map (Boon, Portal, ...) to find the next battle
    """
    global speed
    global threshold

    time.sleep(1.5)

    tempthreshold = threshold
    threshold = 0.95
    if not find_ellement(buttons[7], 1) : # buttons 7: 'play'

        if find_ellement(buttons[21], 14):	# buttons 21: 'reveal'
            time.sleep(1)
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(1.5)

        elif find_ellement(buttons[25], 14):	# buttons 25: 'visit'
            y = windowMP()[1] + windowMP()[3] / 2.2
            time.sleep(1.5)
            while find_ellement_trans(Ui_Ellements[19], 1): # Ui_Ellements 19: 'sombody'
                temp = random.randint(0, 2)
                if temp == 0:
                    x = windowMP()[2] / 2.3
                    pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
                if temp == 1:
                    x = windowMP()[2] / 1.7
                    pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
                if temp == 2:
                    x = windowMP()[2] / 1.4
                    pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.2)
                find_ellement_trans(buttons[18], 14) # buttons 18: 'choose_task'
                time.sleep(5)

        elif find_ellement(Ui_Ellements[24], 14): # Ui_Ellements 24: 'pick'
            time.sleep(1)
            pyautogui.click()
            time.sleep(5)

        elif find_ellement(buttons[19], 14): # Ui_Ellements 24: 'portal-warp'
            time.sleep(1)
#            pyautogui.click()
            time.sleep(5)

        else :
            x, y = pyautogui.position()
            debug("Mouse (x, y) : ", x, y)
            if (y == windowMP()[1] + windowMP()[3] // 2.2) :
                x += windowMP()[2] // 25
                if (x > windowMP()[0] + windowMP()[2]) :
                    x = windowMP()[0] + windowMP()[2] / 3.7
            else :
                x = windowMP()[0] + windowMP()[2] // 3.7
                y = windowMP()[1] + windowMP()[3] // 2.2
            debug("move mouse to (x, y) : ", x, y)
            pyautogui.moveTo(x, y, setings[7])
            time.sleep(0.1)
            pyautogui.click()

    threshold = tempthreshold


def chooseTreasure():
    y = windowMP()[3] / 2
    temp = random.randint(0, 2)
    if temp == 0:
        x = windowMP()[2] / 2.3
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    if temp == 1:
        x = windowMP()[2] / 1.7
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    if temp == 2:
        x = windowMP()[2] / 1.4
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
    pyautogui.click()
    while True:
        if find_ellement_trans(buttons[17], 14):	# buttons 17: 'take'
            time.sleep(1)
            break
        if find_ellement_trans(buttons[28], 14):	# buttons 28: 'keep'
            time.sleep(1)
            break
        if find_ellement_trans(buttons[27], 14):	# buttons 27: 'replace'
            time.sleep(1)
            break



""" Select an ability for a mercenary. Depend on what is available and wich Round (battle)
    Click only on the ability (doesnt move to an enemy)
"""
def abilities(localhero):
    obj='heroes/'+localhero
    if localhero == 'Cariel Roame':
        if raund % 2 == 0:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Antonidas':
        if find_ellement_trans(obj + '/abilics/2.png', 14):
            return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Millhouse Manastorm':
        if raund == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return False
        if raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        if raund > 1:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return False

    elif localhero == 'Tyrande':
        if raund % 2 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
#            if raund % 2 == 0:
#                if find_ellement(obj + '/abilics/3.png', 14):
#                if find_ellement_trans(obj + '/abilics/2.png', 14):
#                    return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Malfurion Stormrage':
        if raund % 2 == 0:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Mannoroth':
        if raund % 3 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return True
        if raund % 3 == 2:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Rathorian':
        if raund == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        elif raund == 2:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        elif raund % 3 == 1:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        elif raund % 3 == 2:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return True
        elif raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Rexxar':
        if raund % 3 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Rokara':
        if raund % 2 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'King Krush' :
        if raund % 3 == 2:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        elif raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return False

    elif localhero == 'Lady Anacondra' :
        if raund % 2 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund % 2 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'War Master Voone':
        if raund % 3 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return True
        if raund % 3 == 2:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Brightwing':
        if raund % 4 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        if raund % 2 == 0:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True
    elif localhero == "Bru'Kan":
        if raund % 3 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund % 3 == 2:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return True
        if raund % 3 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Natalie Seline':
        if raund == 1:
            if find_ellement(obj + '/abilics/1.png', 14):
                return False
        if raund == 3:
            if find_ellement(obj + '/abilics/3.png', 14):
                return False
        if raund > 1:
            if find_ellement(obj + '/abilics/2.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == 'Tamsin Roame':
        if raund == 1:
            if find_ellement(obj + '/abilics/1.png', 14):
                return False
        if raund == 3:
            if find_ellement(obj + '/abilics/3.png', 14):
                return False
        if raund > 1:
            if find_ellement(obj + '/abilics/2.png', 14):
                return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == "Vol'jin":
        if raund == 1:
            if find_ellement(obj + '/abilics/1.png', 14):
                return True
        if raund == 3:
            if find_ellement(obj + '/abilics/3.png', 14):
                return False
        if raund > 1:
            if find_ellement(obj + '/abilics/2.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == "Gul'dan":
        if find_ellement(obj + '/abilics/3.png', 14):
            return True
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    elif localhero == "Mr Smite":
        if raund %3 == 1:
            if find_ellement_trans(obj + '/abilics/1.png', 14):
                return True
        if raund %3 == 2:
            if find_ellement_trans(obj + '/abilics/2.png', 14):
                return False
        if raund %3 == 0:
            if find_ellement_trans(obj + '/abilics/3.png', 14):
                return False
        pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
        pyautogui.click()
        return True

    pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
    pyautogui.click()
    return True


""" Function to attack an enemy (red, green or blue ideally) with the selected mercenary
    red attacks green (if exists)
    green attacks blue (if exists)
    blue attacks red (if exists)
    else merc attacks minion with special abilities or neutral
"""
def attacks(position, mercName, number, enemyred, enemygreen, enemyblue, enemynoclass, mol):
    global mercslist

    debug("[DEBUG] Attacks function")

    print("attack with : ", mercName, "( position :", position, "/", number, ")")
    positionOdd=[640,800,960,1120,1280]
    positionEven=[560,720,880,1040,1200,1360]
    
    if number % 2 == 0 : # if mercenaries are even
        pos= int(2 - (number/2 - 1)  + (position - 1))
        x= int(positionEven[pos])
    else :  # if mercenaries are odd
        pos= int(2 - (number-1)/2 + (position - 1))
        x=int(positionOdd[pos])
    y=windowMP()[1] + windowMP()[3]/1.5

    #print("merclist", mercslist.keys())
    if mercName in mercslist :
        debug("Fight with ",mercName)
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(windowMP()[0] + windowMP()[2]/3, windowMP()[1] + windowMP()[3]/2, setings[7], mouse_random_movement())
        if mercslist[mercName]["type"] == "Protector" :
            if abilities(mercName):
                if move(enemygreen):
                    if move(mol):
                        if move(enemynoclass):
                            rand(enemyred, enemygreen, enemyblue, enemynoclass)
        elif mercslist[mercName]["type"] == "Fighter" :
            if abilities(mercName):
                if move(enemyblue):
                    if move(mol):
                        if move(enemynoclass):
                            rand(enemyred, enemygreen, enemyblue, enemynoclass)
        elif mercslist[mercName]["type"] == "Caster" :
            if abilities(mercName):
                if move(enemyred):
                    if move(mol):
                        if move(enemynoclass):
                            rand(enemyred, enemygreen, enemyblue, enemynoclass)


def battle():
    """ Find the cards on the battlefield (yours and those of your opponents)
        and make them battle until one of yours die
    """
    global raund
    global threshold
    global speed
    global zoneLog
    retour = True

    tempthreshold = threshold
    raund = 1
    while True:
        pyautogui.moveTo(windowMP()[0] + (windowMP()[2] / 2.6), windowMP()[1] + (windowMP()[3] * 0.92), setings[7], mouse_random_movement())
        speed = 0
        threshold = 0.85

        # we look for the (green) "ready" button because :
        # - sometimes, the bot click on it but it doesn't work very well
        # - during a battle, some enemies can return in hand and are put back on battlefield with a "ready" button
        #       but the bot is waiting for a victory / defeat / ... or the yellow button ready
        find_ellement(buttons[14], 14) # buttons 14: 'allready'

        find_ellement(buttons[20], 14) # buttons 20: 'onedie'

        if find_ellement(chekers[13], 1): # chekers 13: 'win'
            retour = 'win'
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
            pyautogui.click()
            zoneLog.cleanBoard()
            
            break
        elif find_ellement(chekers[23], 1): # chekers 23: 'lose'
            retour = 'loose'
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
            pyautogui.click()
            zoneLog.cleanBoard()
            break
        elif find_ellement_trans(buttons[15], 1) or find_ellement_trans(buttons[16], 1):  # buttons 15: 'startbattle' # buttons 16: 'startbattle1'
            # wait 'WaitForEXP' (float) in minutes, to make the battle longer and win more EXP (for the Hearthstone reward track)
            time.sleep(setings[8]) # setings 8: WaitForEXP

            # looks for your Mercenaries on board thanks to log file
            mercenaries = zoneLog.getBoard()
            print("ROUND", raund, " : your board", mercenaries)

            #herobattlefin.clear()

            tmp = int(windowMP()[3] / 2)
            partscreen(int(setings[0].split('x')[0]), tmp, 0, 0) # setings 0: 'MonitorResolution(ex:1920x1080)'

            temp = speed
            threshold = 0.8

            # Look for enemies
            enemyred = find_ellement(Ui_Ellements[9], 12) # Ui_Ellements 9: 'red'
            enemygreen = find_ellement(Ui_Ellements[2], 12) # Ui_Ellements 2: 'green'
            enemyblue = find_ellement(Ui_Ellements[1], 12) # Ui_Ellements 1: 'blue'
            enemynoclass = find_ellement(Ui_Ellements[12], 12) # Ui_Ellements 12: 'noclass'
            mol = find_ellement(Ui_Ellements[11], 12) # Ui_Ellements 11: 'sob'
            print("Enemies : red", enemyred, " - green", enemygreen, " - blue", enemyblue, " - noclass", enemynoclass, " - mol", mol)

            # Go (mouse) to "central zone" and click on an empty space
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            pyautogui.click()
            time.sleep(1)

            for i in mercenaries :
                # Go (mouse) to "central zone" and click on an empty space
                pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
                pyautogui.click()

                attacks(int(i), mercenaries[i], int(list(mercenaries)[-1]), enemyred, enemygreen, enemyblue, enemynoclass, mol)
                time.sleep(0.1)

            threshold = 0.75
            speed = temp
            i = 0
            while True:
                if find_ellement(buttons[14], 14): # buttons 14: 'allready'
                    break
                if i > 10:
                    pyautogui.rightClick()
                    find_ellement_trans(buttons[15], 14) # buttons 15: 'startbattle'
                    break
                time.sleep(0.2)
                i += 1
            time.sleep(3)
            raund += 1
    threshold = tempthreshold
    return retour


def selectCardsInHand():
    """ Select the cards to put on battlefield
        and then, start the 'battle' function
    """

    debug("[ SETH - START]")
    retour = True

    global speed
    global threshold
    heroesOnBattlefield = 0

    while not find_ellement_trans(buttons[5], 2): # buttons 5: 'num'
        time.sleep(0.5)
        
    debug("windowsMP() : ", windowMP())
    x = windowMP()[0] + (windowMP()[2] / 2.6)
    y = windowMP()[1] + (windowMP()[3] * 0.92)
    i = 0
    temp = speed
    speed = 0
    threshold = 0.85
    i = 0
    ## setings 5: 'heroSet(ex:True)'
    #if setings[5] == "True":
    #    while not find_ellement_trans(buttons[14], 1): # buttons 14: 'allready'
    #        threshold = 0.75
    #        pyautogui.moveTo(x, y, setings[7])
    #        for n in range(3):
    #            if i >= 7:
    #                pyautogui.moveTo(windowMP()[0] + (windowMP()[2] / 2), windowMP()[1] + (windowMP()[3] * 0.92), setings[7], mouse_random_movement())
    #                pyautogui.dragTo(windowMP()[0] + (windowMP()[2] / 2), (windowMP()[1] + (windowMP()[3] * 0.92)) - windowMP()[3] / 3, 0.6, mouse_random_movement())
    #                heroesOnBattlefield += 1
    #                break
    #            if find_ellement_trans(hero[n] + '/set.png', 1):
    #                time.sleep(0.2)
    #                pyautogui.dragTo(x, y - windowMP()[3] / 3, 0.6, mouse_random_movement())
    #                heroesOnBattlefield += 1
    #                time.sleep(0.5)
    #                break
    #        else :
    #            x += windowMP()[2] / 22.5
    #            if x > windowMP()[2] / 1.5:
    #                x = windowMP()[0] + (windowMP()[2] / 2.85)
    #        i += 1
    #        if heroesOnBattlefield >= 3 :
    #            break
    #    print('Optout')
    #    speed = temp
    #    threshold = 0.7
    #    pyautogui.moveTo(windowMP()[0] + (windowMP()[2]*0.1), windowMP()[1] + (windowMP()[3]*0.1), setings[7], mouse_random_movement())
    #    time.sleep(1)
    while not find_ellement_trans(buttons[5], 14) :  # buttons 5: 'num'
        pyautogui.moveTo(x, y, setings[7])
        time.sleep(1)
        pyautogui.moveTo(windowMP()[0] + (windowMP()[2]*0.1), windowMP()[1] + (windowMP()[3]*0.1), setings[7], mouse_random_movement())

    retour = battle()
    debug("[ SETH - END]")

    return retour




def travelpointSelection():
    """ Choose a Travel Point (The Barrens, Felwood, ...)
        and the mode : Normal or Heroic
    """
    global threshold
    tempthreshold = threshold
    threshold = 0.65

    if find_ellement(Ui_Ellements[30], 1) : # Ui_Ellements 30: 'travelpoint'

        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())

        pyautogui.scroll(20)
        time.sleep(0.5)

        if setings[2] == "Felwood":	            # setings 2: 'location(ex:TheBarrens)'
            find_ellement(Ui_Ellements[26], 14) # Ui_Ellements 26: 'Felwood'

        elif setings[2] == "Winterspring":        # setings 2: 'location(ex:TheBarrens)'
#            if not find_ellement(Ui_Ellements[25], 14):	# Ui_Ellements 25: 'Winterspring'
            pyautogui.scroll(-2)
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 3, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
            time.sleep(0.5)
            find_ellement(Ui_Ellements[25], 14)	# Ui_Ellements 25: 'Winterspring'
        
        elif setings[2] == "The Barrens":         # setings 2: 'location(ex:TheBarrens)'
            find_ellement(Ui_Ellements[22], 14)	# Ui_Ellements 22: 'Barrens'
        else :
            print("[INFO] Travel Point unknown. The bot won't change the one already selected.")

        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
        time.sleep(0.5)
        
        if setings[3] == "Normal":              # setings 3: 'mode(ex:Heroic)'
            find_ellement(Ui_Ellements[27], 14)	# Ui_Ellements 27: 'normal'
        elif setings[3] == "Heroic":              # setings 3: 'mode(ex:Heroic)'
            find_ellement(Ui_Ellements[28], 14) # Ui_Ellements 28: 'heroic'
        else : 
            print("[INFO] Settings (for Heroic/Normal) unrecognized.")

    waitForItOrPass(buttons[10], 2)
    find_ellement(buttons[10], 14) # buttons 7: 'sta' (= "choose" in Travel Point selection)
    threshold = tempthreshold


def goToEncounter():
    """ Start new fight, continue on the road and collect everything (treasure, rewards, ...) 
    """
    print ("goToEncounter : entering")
    global threshold
    global zoneLog
    time.sleep(2)
    travelEnd=False

    zoneLog = LogHSMercs(setings[9]) # setings 9 : 'ZoneLog' (GameDir/Logs/Zone.log)
    zoneLog.start()
    while not travelEnd :
        tempthreshold = threshold
        threshold = 0.85

        if find_ellement(buttons[7], 14): # buttons 7: 'play'
            time.sleep(0.5)
            threshold = tempthreshold
            retour = selectCardsInHand() # Start the battle : the bot choose the cards and fight against the enemy
            print("goToEncounter - retour = ", retour)
            time.sleep(1)
            if retour == 'win':
                print("goToEncounter : battle won")
                while True:
                    ### ToDo : add a tempo when you detect a new completed task
                    # if find (task completed) :
                    #   time.sleep(2)

                    if not find_ellement_trans(Ui_Ellements[18], 1): # Ui_Ellements 18: 'take_grey'
                        pyautogui.click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if not find_ellement_trans(Ui_Ellements[29], 1): # Ui_Ellements 29: 'replace_grey' (To keep/replace a Treasure?) 
                        pyautogui.click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if find_ellement(Ui_Ellements[31], 1): # Ui_Ellements 31: 'presents_thing' (Look if we killed the boss and won some treasures)
                        print("goToEncounter : Wow! You beat the Boss. Time for REWARDS !!!")
                        collect()
                        travelEnd=True
                        break
            elif retour == 'loose':
                travelEnd=True
                print("goToEncounter : Battle lost")
            else :
                travelEnd=True
                print("goToEncounter : don't know what happened !")
        else :
            threshold = tempthreshold
            nextlvl()
    threshold = tempthreshold
    zoneLog.stop()
    while not find_ellement_trans(buttons[0], 1) : # buttons 0: 'back'
        pyautogui.click()
        time.sleep(1)
    

def travelToLevel():
    """ Go to a Travel Point, choose a level/bounty and go on the road to make encounter

    """

    global threshold

    print("travelToLevel : entering")

    # Look for the level/bounty even if it's on another page
    tempthreshold= threshold
    threshold = 0.65
        
    while find_ellement_trans(Ui_Ellements[20], 1): # Ui_Ellements 20: 'bounties'
        threshold = tempthreshold
        #time.sleep(2)
        if find_ellement("levels/" + setings[2] + "_" + setings[3] + "_" + setings[1] + ".png", 14): # setings 1: 'level(ex:20)'
            waitForItOrPass(buttons[11], 6) # buttons 11: 'start'
            if find_ellement(buttons[11], 14) : # buttons 11: 'start'
                break
        else :
            if find_ellement(buttons[9], 14): # buttons 9: 'sec' (= 'right arrow' (next page))
                time.sleep(1)
                #pass
            else:
                find_ellement(buttons[26], 14) # buttons 26: 'fir' (= 'left arrow' (previous page))
                time.sleep(1)
        threshold = 0.6
    threshold = tempthreshold
    print("travelToLevel ended")
    return

def selectGroup():
    """ Look for the mercenaries group 'Botwork' and select it (click on 'LockIn' if necessary)
    """
    global threshold
    tempthreshold = threshold
    print("selectGroup : entering")
    threshold = 0.8

    if find_ellement(chekers[2], 14): # chekers 2: 'find' ('Botwork' name)
        find_ellement(buttons[12], 14) # buttons 12: 'start1'
        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
        waitForItOrPass(buttons[13], 3) # buttons 13: 'submit' / LockIn
        find_ellement(buttons[13], 14) # buttons 13: 'submit' / LockIn

    threshold = tempthreshold
    debug("selectGroup : ended")
    return


def waitForItOrPass(image, duration):
    """ Wait to find 'image' on screen during 'duration' seconds (max)
            and continue if you don't find it. The purpose is to permit to find a particular part in Hearthstone
            but if the bot doesn't find it, try to go further if you can find another part that it could recognize
    """
    retour = False

    print("Waiting ("+str(duration)+"s max) for : ", image)
    for i in range(duration*2) :
        time.sleep(0.5)
        if find_ellement(image, 1) : # '1' is for 'find it and don't do anything else'
            retour = True
            break
        
    return retour 


def where():
    """ Try to enter in Mercenaries mode, detect where the bot have to resume and go for it 
    """
    global threshold
    tempthreshold = threshold

    find_ellement_trans(buttons[4], 14)   # buttons 4: 'join_button' ("Mercenaries" button on principal menu) => if you find it, click on it

    if find_ellement_trans(chekers[21], 1) : # chekers 21: 'menu'
        time.sleep(4)
        # Find PVE adventure payed and free
        find_ellement_trans(Ui_Ellements[0], 14) or find_ellement_trans(Ui_Ellements[32],14) # Ui_Ellements 0: 'battle' # Ui_Ellements 32: 'free_battle'
        
    threshold = 0.6
    if find_ellement_trans(Ui_Ellements[30], 1) : # Ui_Ellements 30: 'travelpoint'
        threshold = tempthreshold
        time.sleep(3)
        # Find the travel point and the mode (normal/heroic)
        travelpointSelection()
        time.sleep(3)
    threshold = tempthreshold
    
    threshold = 0.65
    if find_ellement_trans(Ui_Ellements[20], 1): # Ui_Ellements 19: 'bounties'
        time.sleep(3)
        threshold = tempthreshold
        travelToLevel()
        time.sleep(3)
    threshold = tempthreshold

    threshold = 0.6
    if find_ellement_trans(Ui_Ellements[33], 1) : # Ui_Ellements 33: 'choose_team'
        time.sleep(3)
        threshold = tempthreshold
        selectGroup()
        time.sleep(3)
    threshold = tempthreshold

    threshold = 0.95
    if find_ellement_trans(buttons[7], 1) : # buttons 7: 'play'
        time.sleep(3)
        threshold = tempthreshold
        goToEncounter()
        time.sleep(3)
    threshold = tempthreshold

    if find_ellement_trans(Ui_Ellements[34], 1) : # Ui_Ellements 33: 'view_party' (button when you are on the road to battle)
        nextlvl()

    #if find_ellement(buttons[5], 1): # buttons 5: 'num'
    #    selectCardsInHand()

    return True


def find_ellement_trans(file, index, threshold="-"):
    """ Find an object ('file') on the screen (UI, Button, ...) and do some actions ('index') 
        support PNG with transparency / alpha channel
        - the old function 'find_ellement' should be deleted
        - need to migrate to this one (find_ellement_trans) and find the right threshold for each image
        - maybe the old find_ellement will be renamed "find_ellement_grey" and will be used for images which could be with different color (silver or gold like heroes cards)
    """
    debug("DEBUG : find_ellement_trans START")
    global screenImg
    global partImg
    global jthreshold
    retour = False
    if threshold == "-" :
        if file in jthreshold : 
            if jthreshold[file] == "-" :
                threshold = jthreshold['default']
            else :
                threshold = jthreshold[file]
        else:
            threshold = jthreshold['default']

    time.sleep(speed)

    # choose if the bot need to look into the screen or in a part of the screen
    if index == 12:
        img = cv2.cvtColor(partImg, cv2.IMREAD_COLOR)
    else:
        screen()
        img = cv2.cvtColor(screenImg, cv2.IMREAD_COLOR)
    
    template_alpha = cv2.imread('files/' + setings[0] + '/' + file, cv2.IMREAD_UNCHANGED)
    template = cv2.cvtColor(template_alpha, cv2.IMREAD_COLOR)
    channels = cv2.split(template_alpha)
    # extract "transparency" channel from image
    alpha_channel = np.array(channels[3])
    # generate mask image, all black dots will be ignored during matching
    mask = cv2.merge([alpha_channel,alpha_channel,alpha_channel])
    result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED, None, mask)

    h = template.shape[0]
    w = template.shape[1]

    loc = np.where(result >= threshold)
    if len(loc[0]) != 0:
        retour = True
        j=0
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x = int((pt[0] * 2 + w) / 2)
        y = int((pt[1] * 2 + h) / 2)
        print("Found " + file, "(", threshold,")", x, y)
        if index == 12 or index == 15:
            retour = (x, y)
        elif index == 2 :
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        elif index == 14 :
            p = random.randint(-2, 2)
            s = random.randint(-2, 2)
            pyautogui.moveTo(x + p, y + s, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
            time.sleep(0.1)
            pyautogui.click()
    else :
        print("Looked for " + file, "(", threshold,")")
        if index == 12 or index == 15:
            retour = (0, 0)
#    print("DEBUG : find_ellement_trans END")
    return retour


def find_ellement(file, index):
    global jthreshold
    debug("DEBUG : find_ellement START")
    if file in jthreshold : 
        retour = find_ellement_trans(file, index, jthreshold[file])
    else :
        retour = find_ellement_grey(file, index)

    debug("DEBUG : find_ellement END")
    return retour

def find_ellement_grey(file, index):
    """ Find an object ('file') on the screen (UI, Button, ...) and do some actions ('index') 
                  FullScreenshot | PartOfTheScreen(shot) |  Actions   | Return
      index = 1 :       x        |                       |     -      | True / False      
      index = 2 :       x        |                       |    move    | True / False
      index = 14:       x        |                       | move+click | True / False
      index = 12:                |           x           |     -      |  x,y / 0,0
      index = 15:       x        |                       |     -      |  x,y / 0,0
        (new index needed to return a tab of object/coordinates)
    """
    debug("DEBUG : find_ellement_grey START")
    global threshold
    global screenImg
    global partImg
    time.sleep(speed)
    retour = False

    # choose if the bot need to look into the screen or in a part of the screen
    if index == 12:
        img = partImg
    else:
        screen()
        img = screenImg

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('files/' + setings[0] + '/' + file, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    h = template.shape[0]
    w = template.shape[1]

    loc = np.where(result >= threshold)
    if len(loc[0]) != 0:
        retour = True
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x = int((pt[0] * 2 + w) / 2)
        y = int((pt[1] * 2 + h) / 2)
        print("Found " + file, "(", threshold,")", x, y)
        if index == 12 or index == 15:
            retour = (x, y)
        elif index == 2 :	
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        elif index == 14 :
            p = random.randint(-2, 2)
            s = random.randint(-2, 2)
            pyautogui.moveTo(x + p, y + s, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
            time.sleep(0.1)
            pyautogui.click()
    else:
        print("Looked for " + file, "(", threshold,")")
        if index == 12 or index == 15:
            retour = (0, 0)
    return retour


def main():
    print("start")
    try:
        configread()
        findgame()
        parslist()
        if(myOS=="windows"):
            ahk.show_info_traytip("started", "all files loaded successfully", slient=False, blocking=True)
            win.show()
            win.restore()
            win.maximize()
            win.to_top()
            win.maximize()
            win.to_top()
            win.activate()
        while True:
            print("Loop")
            if findgame():
                where()
                time.sleep(0.5)
            else:
                print("Game window not found.")
                time.sleep(3)
    except Exception as E:
        print("Error", E)

if __name__ == '__main__':
    main()
