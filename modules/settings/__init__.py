import logging


from .settings import get_settings
from .conf import jthreshold, jposition, mercslist, mercsAbilities, ability_order

log = logging.getLogger(__name__)

# Personalized Settings files
settings_filename = "settings.ini"

"""
Read settings.ini and put it in a table :
Settings -
    0: MonitorResolution (1920x1080),
    1: level (20),
    2: location (The Barrens),
    3: mode (Heroic),
    4: quitBeforeBossFight (True),
    5: stopAtStranger (True),
    6: monitor (1),
    7: MouseSpeed (0.5),
    8: WaitForEXP (3),
    9: Zonelog (GameDir/Logs/Zone.log)
"""
try:
    settings_dict = get_settings(settings_filename)

    log.info("Settings")
    for setting, value in settings_dict.items():
        log.info(f" - {setting}: {value}")

except Exception:
    log.error("Running without settings")


__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
    "settings_dict",
]
