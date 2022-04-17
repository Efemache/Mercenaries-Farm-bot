import os
import logging

from modules.file_utils import readjson, readINI
from modules.utils import update
from modules.exceptions import MissingSettingsFile

log = logging.getLogger(__name__)


BASE_CONFIG_FOLDER = "conf"
USER_CONFIG_FOLDER = "user"
SYSTEM_CONFIG_FOLDER = "system"

config_files = [
    "attacks.json",
    "combo.ini",
    "mercs.json",
    "settings.ini",
    "positions.json",
    "thresholds.json",
]


def get_config(
    base_config_folder=BASE_CONFIG_FOLDER,
    user_folder=USER_CONFIG_FOLDER,
    system_folder=SYSTEM_CONFIG_FOLDER,
    conf_setting_files=config_files,
):
    root_settings_dict = {}

    for setting in conf_setting_files:
        setting_data = {}

        settings_file = os.path.join(base_config_folder, system_folder, setting)
        setting_data = update_settings_with_file(setting_data, settings_file)

        try:
            user_settings_file = os.path.join(base_config_folder, user_folder, setting)
            setting_data = update_settings_with_file(setting_data, user_settings_file)
        except MissingSettingsFile:
            log.debug("No User Settings found for: %s", setting)

        if not setting_data:
            log.info("No Settings found for: %s", setting)

        root_settings_dict[setting] = setting_data

        if setting in ["combo.ini"]:
            log_setting_dict(setting, setting_data)

    return root_settings_dict


def update_settings_with_file(setting_data, new_file):
    if not os.path.exists(new_file):
        raise MissingSettingsFile(f"Settings file: {new_file} not found")

    new_setting_data = readjson(new_file) if new_file[-1] == "n" else readINI(new_file)

    return update(setting_data, new_setting_data)


def log_setting_dict(setting_name, setting_dict):
    log.debug("%s", setting_name)
    log_setting_dict_helper(setting_name, setting_dict)


def log_setting_dict_helper(setting_name, setting_dict, indent=""):
    for setting, value in setting_dict.items():
        if isinstance(value, dict):
            log_setting_dict_helper(setting, value, indent * 4)
        else:
            log.debug(" - %s: %s", setting, value)
