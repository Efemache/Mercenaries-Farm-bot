"""
Conf Subsettings

Handles the various configuration settings files.
This modules receives updated settings
from both system and user setting folders
"""
import logging

from .conf import get_config as _get_config
from .settings import get_updated_settings


_log = logging.getLogger(__name__)

_root_settings_dict = _get_config()


_root_settings_dict["settings.ini"] = get_updated_settings()


_log.debug("Read in conf/ settings")

jthreshold = _root_settings_dict["thresholds.json"]
jposition = _root_settings_dict["positions.json"]
mercslist = _root_settings_dict["mercs.json"]
mercsAbilities = _root_settings_dict["attacks.json"]
ability_order = _root_settings_dict["combo.ini"]
settings_dict = _root_settings_dict["settings.ini"]

__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
    "settings_dict",
]
