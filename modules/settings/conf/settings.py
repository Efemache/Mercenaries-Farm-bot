import logging
import pathlib
import shutil

from modules.exceptions import MissingGameDirectory, UnsetGameDirectory, SettingsError
from modules.file_utils import parseINI, readINI
from modules.utils import update

log = logging.getLogger(__name__)

DEFAULT_RESOLUTION = "1920x1080"
BASE_IMAGES_DIR = "files"


def add_bot_settings(set_dict):
    set_dict["default_resolution"] = DEFAULT_RESOLUTION

    set_dict["root_images_dir"] = BASE_IMAGES_DIR
    set_dict["images_dir"] = pathlib.PurePath(
        BASE_IMAGES_DIR, DEFAULT_RESOLUTION
    ).as_posix()

    set_dict["user_files_dir"] = pathlib.PurePath("conf", "user").as_posix()
    print(set_dict["user_files_dir"])
    print(set_dict["images_dir"])

    return set_dict


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
        else:
            settings_dict["zonelog"] = pathlib.PurePath(
                game_dir, "Logs/Zone.log"
            ).as_posix()

        log.info("Settings")
        for setting, value in settings_dict.items():
            log.info(f" - {setting}: {value}")
    except Exception as e:
        log.error("Running without settings:", e)

    return add_bot_settings(settings_dict)


def get_settings(settings_filename):
    """Read settings.ini and put it in a dict.
    Settings -
        * Resolution (1920x1080),
        * level (20),
        * location (Barrens),
        * mode (Heroic),
        * quitBeforeBossFight (True),
        * monitor (1),
        * MouseSpeed (0.5),
        * WaitForEXP (3),
        * Zonelog (GameDir/Logs/Zone.log)
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
