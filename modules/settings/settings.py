import pathlib
import shutil
import re
import json
import configparser


def readjson(jfile):
    """... just for reading json file and return data :)"""
    with open(jfile) as descriptor:
        data = json.load(descriptor)
    return data


def readINI(inifile, section):
    """... just for reading .ini file and return data"""
    config = configparser.ConfigParser()
    config.read(inifile)

    return config[section]


def parseINI(inidict):
    """... just for transform value into right type"""
    initype = {}
    for k in inidict.keys():
        i = inidict[k].split("#")[0]
        if i in ["True", "False"]:
            initype[k] = bool(i)
        elif re.match("^[0-9]+$", i):
            initype[k] = int(i)
        elif re.match("^[0-9]+\.[0-9]+$", i):
            initype[k] = float(i)
        else:
            initype[k] = str(i)

    return initype


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

    return filename
