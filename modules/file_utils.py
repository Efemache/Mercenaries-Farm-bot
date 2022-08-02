import os
import json
import configparser
import re
import logging
from modules.exceptions import SettingsError

log = logging.getLogger(__name__)


def readjson(jfile):
    """... just for reading json file and return data :)"""
    with open(jfile) as descriptor:
        data = json.load(descriptor)

    return data


def read_ini_to_dict(inifile):
    """read ini file to parsed dictionary"""
    log.debug("Reading %s", inifile)
    return parseINI(readINI(inifile))


def parseINI(inidict):
    """... just for transform value into right type"""
    initype = {}
    for k in inidict.keys():
        i = inidict[k].split("#")[0]
        if i in ["True", "False"]:
            initype[k] = i == "True"
        elif re.match("^[0-9]+$", i):
            initype[k] = int(i)
        elif re.match("^[0-9]+\.[0-9]+$", i):
            initype[k] = float(i)
        else:
            initype[k] = str(i)

    return initype


def readINI(inifile):
    """... just for reading .ini file and return data"""
    config = configparser.ConfigParser()
    try:
        config.read(inifile)
    except configparser.DuplicateOptionError as err:
        log.error("Error while reading ini file %s", err)
        raise SettingsError(f"Duplicate Option in Settings File: {err}") from err

    return config._sections


def copy_dir_and_func_files(rootpath, srcdir, dstdir, ext, func, func_params):
    src = f"{rootpath}/{srcdir}"
    dst = f"{rootpath}/{dstdir}"
    os.path.exists(dst) or os.mkdir(dst)

    for name in os.listdir(src):
        if os.path.isdir(f"{src}/{name}"):
            print(f"Processing directory: {dst}/{name}... wait")
            copy_dir_and_func_files(
                rootpath, f"{srcdir}/{name}", f"{dstdir}/{name}", ext, func, func_params
            )
        else:
            extfile = f"{src}/{name}"
            if extfile.endswith(ext):
                func(extfile, f"{dst}/{name}", func_params)
