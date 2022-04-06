from .conf import get_config as _get_config

_root_settings_dict = _get_config()

jthreshold = _root_settings_dict["thresholds.json"]
jposition = _root_settings_dict["positions.json"]
mercslist = _root_settings_dict["mercs.json"]
mercsAbilities = _root_settings_dict["attacks.json"]
ability_order = _root_settings_dict["combo.ini"]

__all__ = [
    "jthreshold",
    "jposition",
    "mercslist",
    "mercsAbilities",
    "ability_order",
]
