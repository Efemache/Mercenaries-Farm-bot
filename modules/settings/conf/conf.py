import os
import logging

from modules.file_utils import readjson, read_ini_to_dict
from modules.utils import update

log = logging.getLogger(__name__)


base_config_folder = "conf"
user_folder = "user"
system_folder = "system"

conf_setting_files = [
    "attacks.json",
    "combo.ini",
    "mercs.json",
    # "position.ini",
    "positions.json",
    "thresholds.json",
]


def get_config():
    root_settings_dict = {}

    for setting in conf_setting_files:
        setting_data = {}

        settings_file = os.path.join(base_config_folder, system_folder, setting)
        setting_data = update_settings_with_file(setting_data, settings_file)

        user_settings_file = os.path.join(base_config_folder, user_folder, setting)
        setting_data = update_settings_with_file(setting_data, user_settings_file)

        root_settings_dict[setting] = setting_data

    return root_settings_dict


def update_settings_with_file(setting_data, new_file):
    if os.path.exists(new_file):
        if new_file[-1] == "n":
            system_setting_data = readjson(new_file)
        else:
            system_setting_data = read_ini_to_dict(new_file)
        return update(setting_data, system_setting_data)
    else:
        log.debug(f"Settings file: {new_file} not found")

    return setting_data
