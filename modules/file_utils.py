import json
import configparser
import re


def readjson(jfile):
    """... just for reading json file and return data :)"""
    with open(jfile) as descriptor:
        data = json.load(descriptor)
    return data


def read_ini_to_dict(inifile):
    """read ini file to parsed dictionary"""
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
    config.read(inifile)

    return config
