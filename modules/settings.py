"""
Read settings.ini and put it in a table :
Setings -
    0: MonitorResolution (1920x1080),
    1: level (20),
    2: location (The Barrens),
    3: mode (Heroic),
    4: quitBeforeBossFight (True),
    5: heroSet (True),
    6: monitor (1),
    7: MouseSpeed (0.5),
    8: WaitForEXP (3),
    9: Zonelog (GameDir/Logs/Zone.log)
"""
import os
import json
import configparser


settings = {
    "Monitor Resolution": "",
    "level": "",
    "location,": "",
    "mode": "",
    "quitBeforeBossFight": "",
    "heroSet": "",
    "monitor": "",
    "MouseSpeed": "",
    "WaitForEXP": "",
    "Zonelog": "",
}


def configread():
    """Read settings.ini and put it in a table :
        Setings -
            0: MonitorResolution (1920x1080),
            1: level (20),
            2: location (The Barrens),
            3: mode (Heroic),
            4: quitBeforeBossFight (True),
            5: heroSet (True),
            6: monitor (1),
            7: MouseSpeed (0.5),
            8: WaitForEXP (3),
            9: Zonelog (GameDir/Logs/Zone.log)
    Note :Should be replaced with a simple dictionnary to easily find settings
        (actually, you need to find/remember each settings in tab)
    """
    global speed

    config = configparser.ConfigParser()
    config.read("settings.ini")

    speed = float((config["BotSettings"]["bot_speed"]).split("#")[0])

    settings["Monitor Resolution"] = config["BotSettings"][
        "Monitor Resolution"
    ].replace("*", "x")
    for i in ["level", "location", "mode", "quitBeforeBossFight", "heroesSet"]:
        settings[i] = config["BotSettings"][i]

    settings["monitor"] = int(config["BotSettings"]["monitor"])
    settings["MouseSpeed"] = float(config["BotSettings"]["MouseSpeed"])
    settings["WaitForEXP"] = float(config["BotSettings"]["WaitForEXP"]) * 60

    if os.path.exists(config["BotSettings"]["GameDir"] + "/Hearthstone.exe"):
        settings["Zonelog"] = config["BotSettings"]["GameDir"] + "/Logs/Zone.log"
    else:
        print(
            "[ERROR] Set the correct Hearthstone Game Directory in settings.ini"
            " ('GameDir' var)"
        )
        # yeah it's bad coding but don't have time to change everything else
        exit(2)

    print(settings)
    return settings


def readjson(jfile):
    """... just for reading json file and return data :)"""
    with open(jfile) as descriptor:
        data = json.load(descriptor)
    return data


configread()

jthreshold = readjson("conf/thresholds.json")
mercslist = readjson("conf/mercs.json")
mercsAbilities = readjson("conf/attacks.json")
