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
global xm
xm = 0
global ym
ym = 0
global sens
global zipp
global zipchek
zipp = False
zipchek = False
global open
open = False
global createGroup
createGroup = False
sens = 0.75
# for_future=['','','','','','','','','','','','','','','','','','','',]
# Ui-ellements

Ui_Ellements = ['battle', 'blue', 'green', 'group', 'next', 'one', 'page_1', 'page_2', 'page_3', 'red', 'prev', 'sob',
                'noclass', 'bat1', 'bat2', 'bat3', 'bat4', 'bat5', 'findthis', 'sombody', 'pack_open',
                'bounties', 'Barrens', 'startbat', 'pick', 'Winterspring', 'Felwood', 'normal',
                'heroic','replace_grey', 'travelpoint','presents_thing', 'free_battle', 'choose_team']  # noclass 12, bat5-17
# buttons
buttons = ['back', 'continue', 'create', 'del', 'join_button', 'num', 'ok', 'play', 'ready', 'sec', 'sta', 'start',
           'start1', 'submit', 'allready', 'startbattle', 'startbattle1', 'take', 'take1', 'portal-warp', 'onedie', 'reveal',
           'done', 'finishok', 'confirm', 'visit','fir','replace', 'keep']  # last take -17
# chekers
chekers = ['30lvl', 'empty_check', 'find', 'goto', 'group_find', 'level_check', 'rename', 'shab', 'drop', '301', '302',
           'taken', 'text', 'win', 'ifrename', 'levelstarted', 'nextlvlcheck', 'cords-search', '303', '30lvl1',
           '30lvl2', 'menu', 'party','lose']
# Settings - 0: MonitorResolution (1920x1080), 1: level (20), 2: location (The Barrens), 3: mode (Heroic), 4: GroupCreate (True), 5: heroSet (True)
setings = []
# heroes
hero = []
hero_colour = []
pages = ['', '', '']
heroNUM = ['', '', '', '', '', '']
# for battle
herobattle = []
herobattlefin = []
# damp
enemywiz = [0, 0, 0, 0, 0, 0]
heroTEMP = []
# img list
picparser = ['/1.png', '/2.png', '/3.png', '/4.png']

debug_mode=False
def debug(*message):
    if debug_mode :
        print("[DEBUG] ", message)

# window multi-platorm (Windows & Linux support)
def windowMP() :
    if(myOS=='windows'):
        retour=win.rect
    elif(myOS=='linux'):
        retour=win.get_client_window_geometry()
    else:
        retour=None
    return retour

# define function to use mouse on Windows & Linux
def mouse_random_movement():
    return random.choices([pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad])[0]

def configread():
    """ Read settings.ini and put it in a table :
            Setings - 0: MonitorResolution (1920x1080), 1: level (20), 2: location (The Barrens), 3: mode (Heroic), 4: GroupCreate (True), 5: heroSet (True)
    """
    global Resolution
    global speed
    global createGroup
    config = configparser.ConfigParser()
    config.read("settings.ini")
    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])
    n = 0
    for i in ['Red', 'Green', 'Blue']:
        pages[n] = [i, int((config["NumberOfPages"][i]).split("#")[0])]
        n += 1

    setings.append(config["BotSettings"]["Monitor Resolution"].replace('*', 'x'))
    for i in ["level", "location", "mode", "GroupCreate", "heroesSet"]:
        setings.append(config["BotSettings"][i])
    createGroup = setings[4]
    setings.append(int(config["BotSettings"]["monitor"]))
    setings.append(float(config["BotSettings"]["MouseSpeed"]))
    print(setings)
    files = os.listdir('./files/1920x1080/heroes')
    for obj in files:
        for i in range(6):
            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
            if rt != 'auto' and rt != '-':
                if rt == obj.split(".")[0] or rt in obj.split(".")[1]:
                    print(rt)
                    hero.append(obj)
                    hero_colour.append(obj.split(".")[2])
    for n in range(2):
        for i in range(6):
            rt = (config["Heroes"]["hero" + str(i + 1) + "_Number"]).split("#")[0]
            if rt == 'auto' and n==0:
                print(rt)
                hero.append(rt)
                hero_colour.append(rt)
            if rt == '-' and n==1:
                print(rt)
                hero.append(rt)
                hero_colour.append(rt)

    
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
    while i < len(hero):
        hero[i] = "heroes/" + hero[i]
        i += 1
    return 0


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
        #partImg = np.array(sct.grab(monitor))


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

def battlefind(file, coll):
    global partImg
    global sens
    global top
    global left
    herobattle.clear()
    img = partImg                                                                                      
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # преобразуем её в серуюш                        
    template = cv2.imread('files/' + setings[0] + '/' + file, cv2.IMREAD_GRAYSCALE) # объект, который преобразуем в серый, и ищем его на gray_img
    w, h = template.shape[::-1]  # инвертируем из (y,x) в (x,y)`
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= 0.75)
    num = 0
    if len(loc[0]) != 0:
        j = 0
        for pt in zip(*loc[::-1]):
            x = int(((pt[0] * 2 + w) / 2) + 60)
            y = int((((pt[1] * 2 + h) / 2) + (windowMP()[3] / 2)))

            herobattle.append([coll, x, y])
        print("Unsort Data of our heroes", herobattle)

        for i in herobattle:
            print("herobattle : ", i)
            for n in range(6):
                if i[1] < enemywiz[n] + 20 and i[1] > enemywiz[n] - 20:
                    print("first num:", i[1], "second num:", enemywiz[n])
                    if enemywiz[n] != 0:
                        print('then stoped')
                        break
                else:
                    if enemywiz[n] == 0:
                        print("it wrote ", i[1], "in ", enemywiz[num])
                        enemywiz[num] = i[1]
                        print("enemiwiz now", enemywiz)
                        num += 1
                        herobattlefin.append(i)
                        print("herobattle now", herobattlefin)
                        break
        print(enemywiz)
        print("Sort Data of our heroes", herobattlefin)
        for i in range(2):
            enemywiz[i] = 0
        return 0


def move(index):
    if index != (0, 0):
        time.sleep(0.2)
        pyautogui.dragTo(index[0] + 40, index[1] - 30, 0.6, mouse_random_movement())
        debug("Move index (index, x, y) : ",index, index[0] + 40, index[1] - 30)
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
            pyautogui.click()
            break


def collect():
    """ Collect the rewards just after beating the final boss of this level
    """
    global sens
    tmpsens = sens
    sens = 0.65

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
    sens = tmpsens

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
    global sens

    time.sleep(1.5)

    tempsens = sens
    sens = 0.95
    if not find_ellement(buttons[7], 1) : # buttons 7: 'play'

        if find_ellement(buttons[21], 14):	# buttons 21: 'reveal'
            time.sleep(1)
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            pyautogui.click()
            time.sleep(1.5)

        elif find_ellement(buttons[25], 14):	# buttons 25: 'visit'
            y = windowMP()[1] + windowMP()[3] / 2.2
            time.sleep(1.5)
            while find_ellement(Ui_Ellements[19], 1): # Ui_Ellements 19: 'sombody'
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
                time.sleep(0.2)
                find_ellement(buttons[18], 9) # buttons 18: 'take1'
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
                #tm = int(windowMP()[3] / 3.1)
                #partscreen(int(setings[0].split('x')[0]), tm, tm, 0) # setings 0: 'MonitorResolution(ex:1920x1080)'
                x = windowMP()[0] + windowMP()[2] // 3.7
                y = windowMP()[1] + windowMP()[3] // 2.2
            debug("move mouse to (x, y) : ", x, y)
            pyautogui.moveTo(x, y, setings[7])
            pyautogui.click()

#            temp = speed
#            speed = 0
#            for n in range(8):
#                pyautogui.moveTo(x, y, setings[7])
#                pyautogui.click()
#                x += windowMP()[2] / 25
#            speed = temp
#            sens = 0.65
#            for i in range(4):
#                # To Do : here, we could try to find the path to the Mysterious Stranger (Task to win coins for heroes)
#                # ui_ellements 13 - 16 : 'bat1' to 'bat4'
#                x, y = find_ellement(Ui_Ellements[13 + i], 12)
#                if x != 0:
#                    pyautogui.moveTo(x, y + windowMP()[3] / 2.5, setings[7], mouse_random_movement())
#                    pyautogui.click()
#                    break
    sens = tempsens


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
        if find_ellement(buttons[17], 14):	# buttons 17: 'take'
            time.sleep(1)
            break
        if find_ellement(buttons[28], 14):	# buttons 28: 'keep'
            time.sleep(1)
            break
        if find_ellement(buttons[27], 14):	# buttons 27: 'replace'
            time.sleep(1)
            break


def resize():
    for i in range(6):
        if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            image_path = './files/' + setings[0] + '/' + hero[i] + '/set.png'
            img = Image.open(image_path)
            # получаем ширину и высоту
            width, height = img.size
            print(width, height)
            # открываем картинку в окне
            new_image = img.resize((int(width * 0.65), int(height * 0.65)))
            new_image1 = img.resize((int(width * 0.75), int(height * 0.75)))
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            new_image.save('./files/' + setings[0] + '/' + hero[i] + '/main.png')
	# setings 0: 'MonitorResolution(ex:1920x1080)'
            new_image1.save('./files/' + setings[0] + '/' + hero[i] + '/group.png')


def abilicks(index):
    heroTEMP.clear()
    for i in range(3):
        if hero_colour[i] == index:
            heroTEMP.append(hero[i])
    print(index)
    print("Hero dump",heroTEMP)
    for obj in heroTEMP:
        if obj == 'heroes/1.Cariel Roame.Red':
            if raund > 1 and raund % 2 == 0:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return False
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True

        elif obj == 'heroes/3.Milhous Manashtorm.Blue':
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

        elif obj == 'heroes/2.Tirande.Green':
            if raund % 2 == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return True
            if raund % 2 == 0:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True
        elif obj == 'heroes/38':
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
        elif obj == 'heroes/40':
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
        elif obj == 'heroes/42':
            if raund == 1:
                if find_ellement(obj + '/abilics/1.png', 14):
                    return False
            if raund == 3:
                if find_ellement(obj + '/abilics/3.png', 14):
                    return False
            if raund > 1:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return True
        #elif obj == 'heroes/44':
        elif obj == 'heroes/44.Gul\'dan.Blue':
            if raund %2 == 0:
                if find_ellement(obj + '/abilics/2.png', 14):
                    return False
            pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
            pyautogui.click()
            return True
                
    pyautogui.moveTo(int(windowMP()[0] + windowMP()[2] / 2.5), int(windowMP()[1] + windowMP()[2] / 4), setings[7], mouse_random_movement())
    pyautogui.click()
    return True


def atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol):
    x = int(i[1])
    y = int(i[2])
    print("Attack function")
    if i[0] == 'Red':
        print("open Red")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        if abilicks('Red'):
            if move(enemygreen):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Green':
        print("open Green")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        if abilicks('Green'):
            if move(enemyblue):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)
    if i[0] == 'Blue':
        print("open blue")
        pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        pyautogui.click()
        time.sleep(0.2)
        if abilicks('Blue'):
            if move(enemyred):
                if move(mol):
                    if move(enemynoclass):
                        rand(enemyred, enemygreen, enemyblue, enemynoclass)


def battle():
    """ Find the cards on the battlefield (yours and those of your opponents)
        and make them battle until one of yours die
    """
    global raund
    global sens
    global zipchek
    global speed
    retour = True

    tempsens = sens
    raund = 1
    while True:
        pyautogui.moveTo(windowMP()[0] + (windowMP()[2] / 2.6), windowMP()[1] + (windowMP()[3] * 0.92), setings[7], mouse_random_movement())
        speed = 0
        sens = 0.85

        # we look for the (green) "ready" button because :
        # - sometimes, the bot click on it but it doesn't work very well
        # - during a battle, some enemies can return in hand and are put back on battlefield with a "ready" button
        #       but the bot is waiting for a victory / defeat / ... or the yellow button ready
        # buttons 14: 'allready'
        find_ellement(buttons[14], 2)

        find_ellement(buttons[20], 14) # buttons 20: 'onedie'

        if find_ellement(chekers[13], 1): # chekers 13: 'win'
            retour = 'win'
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
            pyautogui.click()
            break
        elif find_ellement(chekers[23], 1): # chekers 23: 'lose'
            retour = 'loose'
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.6, setings[7], mouse_random_movement())
            pyautogui.click()
            break
        elif find_ellement(buttons[15], 1) or find_ellement(buttons[16], 1):  # buttons 15: 'startbattle' # buttons 16: 'startbattle1'
            herobattlefin.clear()

            tmp = int(windowMP()[3] / 2)
            partscreen(int(setings[0].split('x')[0]), tmp, 0, 0) # setings 0: 'MonitorResolution(ex:1920x1080)'

            temp = speed
            sens = 0.8

            # Look for enemies
            enemyred = find_ellement(Ui_Ellements[9], 12) # Ui_Ellements 9: 'red'
            enemygreen = find_ellement(Ui_Ellements[2], 12) # Ui_Ellements 2: 'green'
            enemyblue = find_ellement(Ui_Ellements[1], 12) # Ui_Ellements 1: 'blue'
            enemynoclass = find_ellement(Ui_Ellements[12], 12) # Ui_Ellements 12: 'noclass'
            print("red: ", enemyred)
            print("green: ", enemygreen)
            print("blue: ", enemyblue)
            print("noclass: ", enemynoclass)
            # Ui_Ellements 11: 'sob'
            mol = find_ellement(Ui_Ellements[11], 12)
            # Go (mouse) to "central zone" and click on an empty space
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
            pyautogui.click()
            time.sleep(1)
            # setings 0: 'MonitorResolution(ex:1920x1080)'
            partscreen(int(setings[0].split('x')[0]), tmp, tmp, 0)
            # setings 0: 'MonitorResolution(ex:1920x1080)'
            print("enter serch Red")
            # Ui_Ellements 9: 'red'
            battlefind(Ui_Ellements[9], 'Red')  # find all yr Red
            if len(herobattlefin) != 3:
                print("enter serch Green")
                # Ui_Ellements 2: 'green'
                battlefind(Ui_Ellements[2], 'Green')  # find all yr Green
            if len(herobattlefin) != 3:
                print("enter serch Blue")
                # Ui_Ellements 1: 'blue'
                battlefind(Ui_Ellements[1], 'Blue')  # find all yr Blue
            print("cords of my heroes ")
            print(herobattlefin)
            for i in herobattlefin:
                # Go (mouse) to "central zone" and click on an empty space
                pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] - windowMP()[3] / 4.8, setings[7], mouse_random_movement())
                pyautogui.click()
                debug("print atack", i, enemyred, enemygreen, enemyblue, enemynoclass, mol)
                atack(i, enemyred, enemygreen, enemyblue, enemynoclass, mol)
                time.sleep(0.1)
            sens = 0.75
            speed = temp
            i = 0
            while True:
                if not find_ellement(buttons[14], 2): # buttons 14: 'allready'
                    break
                if i > 10:
                    pyautogui.rightClick()
                    if(myOS=='windows'):
                        ahk.show_warning_traytip("Battle", "Battle error,please write what happend on github issue")
                    else :
                        print("Battle error,please write what happend on github issue")
                    find_ellement(buttons[15], 2) # buttons 15: 'startbattle'
                    break
                time.sleep(0.2)
                i += 1
            time.sleep(3)
            raund += 1
    sens = tempsens
    return retour


def seth():
    """ Select the cards to put on battlefield
        and then, start the 'battle' function
    """

    debug("[ SETH - START]")
    retour = True

    global speed
    global sens
    while not find_ellement(buttons[5], 1): # buttons 5: 'num'
        time.sleep(0.5)
        
    debug("windowsMP() : ", windowMP())
    x = windowMP()[0] + (windowMP()[2] / 2.6)
    y = windowMP()[1] + (windowMP()[3] * 0.92)
    i = 0
    temp = speed
    speed = 0
    sens = 0.85
    i = 0
    # setings 5: 'heroSet(ex:True)'
    if setings[5] == "True":
        # buttons 14: 'allready'
        while not find_ellement(buttons[14], 1):
            print('Entrance')
            sens = 0.75
            pyautogui.moveTo(x, y, setings[7])
            #debug("mouse move to : ", x, y, setings[7])
            for n in range(3):
                if i >= 7:
                    pyautogui.moveTo(windowMP()[0] + (windowMP()[2] / 2), windowMP()[1] + (windowMP()[3] * 0.92), setings[7], mouse_random_movement())
                    pyautogui.dragTo(windowMP()[0] + (windowMP()[2] / 2), (windowMP()[1] + (windowMP()[3] * 0.92)) - windowMP()[3] / 3, 0.6, mouse_random_movement())
                    break
                if find_ellement(hero[n] + '/set.png', 6):
                    time.sleep(0.2)
                    pyautogui.dragTo(x, y - windowMP()[3] / 3, 0.6, mouse_random_movement())
                    time.sleep(0.5)
                    break
            else :
                x += windowMP()[2] / 22.5
                if x > windowMP()[2] / 1.5:
                    x = windowMP()[0] + (windowMP()[2] / 2.85)
            i += 1
        print('Optout')
        speed = temp
        sens = 0.7
        pyautogui.moveTo(windowMP()[0] + (windowMP()[2]*0.1), windowMP()[1] + (windowMP()[3]*0.1), setings[7], mouse_random_movement())
        time.sleep(1)
    retour = battle()
    debug("[ SETH - END]")

    return retour




def travelpointSelection():
    """ Choose a Travel Point (The Barrens, Felwood, ...)
        and the mode : Normal or Heroic
    """
    global sens
    tempsens = sens
    sens = 0.65

    waitForItOrPass(Ui_Ellements[30], 6) # Ui_Ellements 30: 'travelpoint'
    if find_ellement(Ui_Ellements[30], 1) : # Ui_Ellements 30: 'travelpoint'

        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())

        pyautogui.scroll(20)
        time.sleep(0.5)

        if setings[2] == "Felwood":	            # setings 2: 'location(ex:TheBarrens)'
            find_ellement(Ui_Ellements[26], 14) # Ui_Ellements 26: 'Felwood'

        if setings[2] == "Winterspring":        # setings 2: 'location(ex:TheBarrens)'
            find_ellement(Ui_Ellements[25], 14)	# Ui_Ellements 25: 'Winterspring'
        
        if setings[2] == "The Barrens":         # setings 2: 'location(ex:TheBarrens)'
            find_ellement(Ui_Ellements[22], 14)	# Ui_Ellements 22: 'Barrens'
        else :
            print("[INFO] Travel Point unknown. The bot won't change the one already selected.")

        pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 2, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
        time.sleep(0.5)
        
        if setings[3] == "Normal":              # setings 3: 'mode(ex:Heroic)'
            find_ellement(Ui_Ellements[27], 14)	# Ui_Ellements 27: 'normal'
        if setings[3] == "Heroic":              # setings 3: 'mode(ex:Heroic)'
            find_ellement(Ui_Ellements[28], 14) # Ui_Ellements 28: 'heroic'
        else : 
            print("[INFO] Settings (for Heroic/Normal) unrecognized.")
        time.sleep(1)

    find_ellement(buttons[10], 14) # buttons 7: 'sta' (= "choose" in Travel Point selection)
    sens = tempsens


def goToEncounter():
    """ Start new fight, continue on the road and collect everything (treasure, rewards, ...) 
    """
    print ("goToEncounter : entering")
    global sens
    time.sleep(2)
    travelEnd=False
    while not travelEnd :
        tempsens = sens
        sens = 0.85
        if find_ellement(buttons[7], 14): # buttons 7: 'play'
            time.sleep(0.5)
            sens = tempsens
            retour = seth() # Start the battle : the bot choose the cards and fight against the enemy
            print("goToEncounter - retour = ", retour)
            time.sleep(1)
            if retour == 'win':
                print("goToEncounter : battle won")
                while True:
                    ### ToDo : add a tempo when you detect a new completed task
                    # if find (task completed) :
                    #   time.sleep(2)

                    if not find_ellement(Ui_Ellements[18], 1): # Ui_Ellements 18: 'findthis' ('Take' grey button)
                        pyautogui.click()
                        time.sleep(0.5)
                    else:
                        chooseTreasure()
                        break

                    if not find_ellement(Ui_Ellements[29], 1): # Ui_Ellements 29: 'replace_grey' (To keep/replace a Treasure?) 
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
            sens = tempsens
            nextlvl()


def travelToLevel():
    """ Go to a Travel Point, choose a level/bounty and go on the road to make encounter

    """

    global sens

    print("travelToLevel : entering")

    # Find PVE adventure payed and free
    find_ellement(Ui_Ellements[0], 14) or find_ellement(Ui_Ellements[32],14) # Ui_Ellements 0: 'battle' # Ui_Ellements 32: 'free_battle'
    time.sleep(1)

    # Find the travel point and the mode (normal/heroic)
    #pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
    travelpointSelection()

    # Look for the level/bounty even if it's on another page
    tempsens= sens
    sens = 0.65
        
    waitForItOrPass(Ui_Ellements[21], 6) # Ui_Ellements 21: 'bounties'
    while find_ellement(Ui_Ellements[21], 1) : # Ui_Ellements 21: 'bounties'
        #time.sleep(1)
        if find_ellement("levels/" + setings[2] + "_" + setings[3] + "_" + setings[1] + ".png", 14): # setings 1: 'level(ex:20)'
            waitForItOrPass(buttons[11], 4) # buttons 11: 'start'
            find_ellement(buttons[11], 14) # buttons 11: 'start'
            break
        else :
            if find_ellement(buttons[9], 2): # buttons 9: 'sec' (= 'right arrow' (next page))
                time.sleep(1)
                #pass
            else:
                find_ellement(buttons[26], 2) # buttons 26: 'fir' (= 'left arrow' (previous page))
                time.sleep(1)

    sens = 0.5
    # Look for the mercenaries group 'Botwork' and select it (with 'LockIn' if necessary)
    waitForItOrPass(Ui_Ellements[33], 6) # Ui_Ellements 33: 'choose_team'
    sens = 0.75
    while True:
        if not find_ellement(chekers[2], 2): # chekers 2: 'find'
            find_ellement(buttons[12], 2) # buttons 12: 'start1'
            pyautogui.moveTo(windowMP()[0] + windowMP()[2] / 1.5, windowMP()[1] + windowMP()[3] / 2, setings[7], mouse_random_movement())
            time.sleep(1.5)
            find_ellement(buttons[13], 14) # buttons 13: 'submit' / LockIn
            break
    sens = tempsens

    print("travelToLevel ended")
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
    """ Try to enter in Mercenaries mode and to create a group of heroes if
    configured in settings.ini
    """
    global createGroup

    if waitForItOrPass(buttons[4], 6) : # buttons 4: 'join_button' | "Mercenaries" button on principal menu
        find_ellement(buttons[4], 14)   # if you find it, click on it

    # check if we need to create a group of Mercenaries
    if createGroup == 'True':
        print("where : create a group of mercenaries")
        waitForItOrPass(Ui_Ellements[3], 2)  # Ui_Ellements 3: 'group'
        if find_ellement(Ui_Ellements[3], 14) : # Ui_Ellements 3: 'group'
            time.sleep(2)
            if group_create() :
                createGroup = 'False'
    else :
        
        waitForItOrPass(chekers[21], 6) # chekers 21: 'menu'
        travelToLevel()
        time.sleep(2)
        goToEncounter()
        time.sleep(2)

        while not find_ellement(chekers[21], 1) :	# chekers 21: 'menu'
            pyautogui.click()
            time.sleep(1)
            find_ellement(buttons[0], 14) # buttons 0: 'back'
#        goToEncounter()
#        while not find_ellement(chekers[21], 1) :	# chekers 21: 'menu'
#            pyautogui.click()
#            time.sleep(0.5)
#            find_ellement(buttons[0], 14) # buttons 0: 'back'
            
    return True


def pagech(page, coll):
    print("hero number is", coll)
    print(hero_colour[coll])
    print(pages)
    for i in pages:
        if hero_colour[coll] in i:
            print("color found")
            num = i[1]
            print(num)
    if int(num) > 1:
        if page != num:
	# Ui_Ellements 4: 'next'
            find_ellement(Ui_Ellements[4], 0)
            time.sleep(1)
            page += 1
        else:
            while page != 1:
	# Ui_Ellements 10: 'prev'
                find_ellement(Ui_Ellements[10], 0)
                page -= 1
                time.sleep(1)
    return page


def find(n):
    global speed
    temp = speed
    speed = 0
    change(n)
    page = 1
    attempt = 0
    while True:
        attempt += 1
        if attempt > 4:
            change(n)
        if find_ellement(hero[n] + "/main.png", 6):
            print('find (function)')
            find_ellement(chekers[8], 14)	# chekers 8: 'drop'
            return True
        else:
            page = pagech(page, n)
    speed = temp


def change(index):
    if hero_colour[index] == 'Red':
        find_ellement(Ui_Ellements[6], 9) # Ui_Ellements 6: 'page_1'
    if hero_colour[index] == 'Green':
        find_ellement(Ui_Ellements[7], 9)	# Ui_Ellements 7: 'page_2'
    if hero_colour[index] == 'Blue':
        find_ellement(Ui_Ellements[8], 9)	# Ui_Ellements 8: 'page_3'
    print("page change for hero", index)
    time.sleep(1)


def group_create():
    """ Create group of mercenaries / heroes
    """
    global speed
    global left
    global top
    global sens
    retour = False

    if find_ellement(chekers[22], 1): # chekers 22: 'party'
        retour = True
        # chekers 4: 'group_find'
        if find_ellement(chekers[4], 3) == 6:
        # buttons 2: 'create'
            find_ellement(buttons[2], 0)
            time.sleep(1.5)
            print(windowMP())
            x = int(windowMP()[2] / 1.3)
            y = int(windowMP()[3] / 9)
        # chekers 14: 'ifrename'
            # while not find_ellement(chekers[14], 14):
            pyautogui.moveTo(windowMP()[0] + x, windowMP()[1] + y, setings[7], mouse_random_movement())
            time.sleep(0.5)
            pyautogui.click()
            temp = speed
            speed = 0
            #ahk.send_input('Botwork', 0)
            pyautogui.write('Botwork', interval=0.25)
        # Ui_Ellements 10: 'prev'
            find_ellement(Ui_Ellements[10], 0)
            time.sleep(1)
            fx=0
            for i in range(6):
                if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
                    print("Starting adding hero ", i)
                    find(i)
                if hero[i] == 'heroes/auto':
                    fx += 1
            print('how many auto',fx)
            if fx != 0:
                print("Add heroes")
        # Ui_Ellements 6: 'page_1'
                find_ellement(Ui_Ellements[6], 14)
                time.sleep(0.5)
                find_merc(fx)
            speed = temp
        # buttons 8: 'ready'
            find_ellement(buttons[8], 0)
            time.sleep(0.2)
        # buttons 1: 'continue'
            find_ellement(buttons[1], 0)
            time.sleep(0.2)
        # Ui_Ellements 6: 'page_1'
            find_ellement(Ui_Ellements[6], 2)
        else:
            time.sleep(1)
        # chekers 17: 'cords-search'
            x, y = find_ellement(chekers[17], 15)
            x = x - int(windowMP()[2] / 9)
            y = y + int(windowMP()[3] / 18.5)
            add = 0
            herocust = 0
            autoadd = 0
            temphero = []
            for i in range(6):
                if hero[i] != 'heroes/auto' and hero[i] != 'heroes/-':
                    herocust += 1
                if hero[i] == 'heroes/auto':
                    autoadd += 1
            for i in range(herocust + autoadd):
                temp = sens
                sens = 0.65
                pyautogui.moveTo(x, y, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
                pyautogui.click()
                if i <= herocust - 1:
                    bool_check = False
                    time.sleep(0.2)
                    for i in range(herocust):
                        if find_ellement(hero[i] + "/group.png", 1):
                            bool_check = True
                            temphero.append(i)
                            y = y + int(windowMP()[3] / 19)
                    print("Temphero is ",temphero)
                    if bool_check is False:
                        sens = 0.85
                        pyautogui.dragTo(x - 600, y, 0.6, mouse_random_movement())
                    sens = temp
                if i > autoadd - 1:
                    temp = sens
                    sens = 0.85
                    time.sleep(0.5)
        # chekers 0: '30lvl'
        # chekers 19: '30lvl1'
        # chekers 20: '30lvl2'
                    if find_ellement(chekers[0], 1) or find_ellement(chekers[19], 1) or find_ellement(chekers[20], 1):
                        pyautogui.dragTo(x - 600, y, 0.6, mouse_random_movement())
                        add += 1
                    else:
                        y = y + int(windowMP()[3] / 17.2)
            sens = 0.7
        # buttons 8: 'ready'
            find_ellement(buttons[8], 14)
            time.sleep(0.5)
            for i in range(herocust):
                if i not in temphero:
                    print("Find hero with index ", i)
                    find(i)
            if add != 0:
                print("Add heroes")
        # Ui_Ellements 6: 'page_1'
                find_ellement(Ui_Ellements[6], 14)
                time.sleep(0.5)
                find_merc(add)
            while True:
        # buttons 8: 'ready'
                if find_ellement(buttons[8], 14):
                    time.sleep(0.5)
        # buttons 1: 'continue'
                    find_ellement(buttons[1], 14)
                    break
        # chekers 21: 'menu'
            while not chekers[21]:
        # buttons 0: 'back'
                find_ellement(buttons[0],14)
                time.sleep(0.5)
            sens = temp
            time.sleep(0.5)
    
    return retour

def find_merc(n):
    time.sleep(0.5)
    global left
    global top
    global speed
    global sens
    i = 0
    temp1 = sens
    sens = 0.9
    temp = speed
    speed = 0
    while i < n:
        print("enter iteration loop")
        x = int(windowMP()[2] / 7.5)
        y = int(windowMP()[3] / 3.5)
        top = int(windowMP()[3] / 5.76)
        left = int(windowMP()[2] / 5.2)
        h = 0
        while h < 2:
            print("enter height loop")
            left = int(windowMP()[2] / 5.2)
            j = 0
            while j < 3:
                if i >=n:
                    break
                print("enter width loop")
                partscreen(x, y, top, left)
                if find_ellement(chekers[12], 7):	# chekers 12: 'text'
                    print(xm, ym)
                    # chekers 9: '301' # chekers 10: '302' # chekers 18: '303'
                    if find_ellement(chekers[9], 7) is False and find_ellement(chekers[10],7) is False and find_ellement(chekers[18], 7) is False:
                        print("found object")
                        if not find_ellement(chekers[11], 7): # chekers 11: 'taken'
                            find_ellement(chekers[8], 7) # chekers 8: 'drop'
                            i += 1
                            print("droped the object")

                j += 1
                left += int(windowMP()[2] / 7)
                print("go next element on line")
            top += int(windowMP()[3] / 3)
            print("go next line")
            h += 1
        find_ellement(Ui_Ellements[4], 0) # Ui_Ellements 4: 'next'
    speed = temp
    sens = temp1


def find_ellement(file, index):
    global sens
    global top
    global left
    global screenImg
    global partImg
    time.sleep(speed)

    # choose if the bot need to look into the screen or in a part of the screen
    if index == 12:
        img = partImg 
    elif index == 7 and file != chekers[8]: # chekers 8: 'drop'
        img = partImg 
    else:
        screen()
        img = screenImg

#    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                # Transform the image in grey; that's how CV2 will find the match
#    template = cv2.imread('files/' + setings[0] + '/' + file, cv2.IMREAD_GRAYSCALE) # setings 0: 'MonitorResolution(ex:1920x1080)'
#    w, h = template.shape[::-1]  # inverse (y,x) to (x,y)
#    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pngfile = cv2.imread('files/1920x1080/' + file)
    template = cv2.cvtColor(pngfile, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    try:
        # look if the png file has alpha channel
        IMG_RED, IMG_GREEN, IMG_BLUE, IMG_ALPHA = cv2.split(pngfile)
        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED, pngfile)
    except:
        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= sens)
    if len(loc[0]) != 0:
        for pt in zip(*loc[::-1]):
            pt[0] + w
            pt[1] + h
        x = int((pt[0] * 2 + w) / 2)
        y = int((pt[1] * 2 + h) / 2)
        print("Found " + file, x, y)
        if index == 12 or index == 15:
            return (x, y)
        if (index == 6 or file == Ui_Ellements[5] or file == chekers[7]):	# chekers 7: 'shab' # Ui_Ellements 5: 'one'
            global xm
            global ym
            xm = x
            ym = y
            return True
        if file == chekers[8]:	# chekers 8: 'drop'
            if index == 7:
                xm += left
                ym += top
            pyautogui.moveTo(xm, ym, setings[7], mouse_random_movement())
            time.sleep(0.5)
            if index== 14:
                y=windowMP()[1] + y-windowMP()[3]/1.9
            pyautogui.dragTo(x, y, 0.6, mouse_random_movement())
            return True
        if file == chekers[5]:	# chekers 5: 'level_check'
            pyautogui.moveTo(x, y + 70, setings[7], mouse_random_movement())
            pyautogui.click()
            return True
        if file == buttons[5]:	# buttons 5: 'num'
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
            return True
        if file == chekers[3]:	# chekers 3: 'goto'
            pyautogui.moveTo(x, y, setings[7], mouse_random_movement())
        if index == 1:
            return True
        if index == 7:
            xm = x
            ym = y
            return True
        p = random.randint(-2, 2)
        s = random.randint(-2, 2)
        pyautogui.moveTo(x + p, y + s, setings[7], mouse_random_movement())  # Moves the mouse instantly to absolute screen position
        time.sleep(0.1)
        pyautogui.click()
        if file == buttons[7]:	# buttons 7: 'play'
            return True
        if index == 14:
            return True
    else:
        print("Not found  " + file)
        if index == 14:
            return False
        if index == 12 or index == 15:
            return 0, 0
        if index == 6:
            return False
        if index == 7:
            return False
        if index == 3:
            return 6
        if index == 2:
            return True
        if index == 1 or index == 9 or index == 12:
            return False
        if file == buttons[7]:	# buttons 7: 'play'
            return False

    #    if file != buttons[4] and file != Ui_Ellements[3] and file != buttons[0]:	# buttons 0: 'back' # buttons 4: 'join_button' # Ui_Ellements 3: 'group'
    #        where()



def main():
    print("start")
    try:
        #ahk.show_info_traytip("Starting", "loading files", slient=False, blocking=True)
        configread()
        findgame()
        parslist()
        resize()
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
            print("Loop start")
            if findgame():
                where()
            else:
                print("Not found Game window.")
                time.sleep(5)
    except Exception as E:
        print("Error", E)

if __name__ == '__main__':
    main()
