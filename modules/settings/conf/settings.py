import logging
import pathlib
import shutil

from modules.exceptions import MissingGameDirectory, UnsetGameDirectory, SettingsError
from modules.file_utils import parseINI, readINI
from modules.utils import update

log = logging.getLogger(__name__)


def get_system_user_settings(system_settings_filename, user_settings_filename):
    try:
        system_settings_dict = get_settings(system_settings_filename)
        user_settings_dict = get_settings(user_settings_filename)
        settings_dict = update(system_settings_dict, user_settings_dict)
        if not settings_dict["gamedir"]:
            raise UnsetGameDirectory("Game Dir setting is not set")

        game_dir = pathlib.Path(settings_dict["gamedir"])
        if not game_dir.is_dir():
            raise MissingGameDirectory(f"Game directory ({game_dir}) does not exist")

        log.info("Settings")
        for setting, value in settings_dict.items():
            log.info(f" - {setting}: {value}")
    except Exception as e:
        log.error("Running without settings")

    return settings_dict


def get_settings(settings_filename):
    """Read settings.ini and put it in a table :
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
    raw_settings = readINI(settings_filename)

    try:
        settings_dict = parseINI(raw_settings["BotSettings"])
    except KeyError as kerr:
        log.error(f"Settings file is missing section {kerr}")
        raise SettingsError(f"Settings file is missing section {kerr}") from kerr

    return settings_dict


def copy_config_from_sample_if_not_exists(filename):
    """Copy Sample config to config if config doesn't exist

    If file exists, do nothing, else copy sample to file

    Args:
        filename (str): config filename
    """
    filepath = pathlib.Path(filename)

    if not filepath.is_file():
        sample_file = f"{filename}.sample"
        samplepath = pathlib.Path(sample_file)
        if samplepath.is_file():
            shutil.copy(samplepath, filepath)

    return filepath.as_posix()
