"""
Conf Subsettings

Handles the various configuration settings files.
This modules receives updated settings
from both system and user setting folders
"""
import logging

from .conf import get_config as _get_config


_log = logging.getLogger(__name__)

_log.debug("Read in conf/ settings")
_root_settings_dict = _get_config()


jthreshold = _root_settings_dict["thresholds.json"]
jposition = _root_settings_dict["positions.json"]
mercslist = _root_settings_dict["mercs.json"]
mercsAbilities = _root_settings_dict["attacks.json"]
ability_order = _root_settings_dict["combo.ini"]
settings_dict = _root_settings_dict["settings.ini"]
treasures_priority = _root_settings_dict["treasures.json"]

__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
    "settings_dict",
    "treasures_priority",
]
