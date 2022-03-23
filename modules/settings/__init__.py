from .settings import copy_config_from_sample_if_not_exists, readjson, parseINI, readINI

# Personalized Settings files
settings_filename = "settings.ini"
image_threshold_filename = "conf/thresholds.json"
combo_filename = "conf/combo.ini"

# Standard Files
mercslist_filename = "conf/mercs.json"
attacks_filename = "conf/attacks.json"

personalized_files = [
    settings_filename,
    image_threshold_filename,
    combo_filename,
]

for file in personalized_files:
    copy_config_from_sample_if_not_exists(file)

"""Read settings.ini and put it in a table :
    Settings -
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
settings_dict = parseINI(readINI(settings_filename, "BotSettings"))
settings_dict["zonelog"] = f"{settings_dict['gamedir']}/Logs/Zone.log"

jthreshold = readjson(image_threshold_filename)
mercslist = readjson(mercslist_filename)
mercsAbilities = readjson(attacks_filename)

print("Settings")
for setting, value in settings_dict.items():
    print(f" - {setting}: {value}")
