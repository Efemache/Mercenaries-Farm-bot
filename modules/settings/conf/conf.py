import os
import logging

from modules.file_utils import readjson, readINI
from modules.utils import update
from modules.exceptions import MissingSettingsFile

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


def get_config(
    base_config_folder=base_config_folder,
    user_folder=user_folder,
    system_folder=system_folder,
    conf_setting_files=conf_setting_files,
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
        log.debug("%s", setting)
        for setting, value in setting_data.items():
            log.debug(f" - {setting}: {value}")

    return root_settings_dict


def update_settings_with_file(setting_data, new_file):
    if not os.path.exists(new_file):
        raise MissingSettingsFile(f"Settings file: {new_file} not found")

    new_setting_data = readjson(new_file) if new_file[-1] == "n" else readINI(new_file)

    return update(setting_data, new_setting_data)
