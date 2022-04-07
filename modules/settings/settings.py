import pathlib
import shutil

from modules.exceptions import MissingGameDirectory, UnsetGameDirectory
from modules.file_utils import parseINI, readINI


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
    settings_dict = parseINI(readINI(settings_filename)["BotSettings"])

    if not settings_dict["gamedir"]:
        raise UnsetGameDirectory("Game Dir setting is not set")

    game_dir = pathlib.Path(settings_dict["gamedir"])

    if not game_dir.is_dir():
        raise MissingGameDirectory(f"Game directory ({game_dir}) does not exist")
    else:
        settings_dict["zonelog"] = pathlib.PurePath(
            game_dir, "Logs/Zone.log"
        ).as_posix()

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
