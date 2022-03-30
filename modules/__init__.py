import logging
import logging.config

log_config = {
    "version": 1,
    "root": {
        "handlers": [
            "console",
            # "file"
        ],
        "level": "DEBUG",
    },
    "handlers": {
        "console": {
            "formatter": "old_out",
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
        "file": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "mfb.log",
        },
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S",
        },
        "old_out": {"format": "%(message)s"},
    },
}

logging.config.dictConfig(log_config)
