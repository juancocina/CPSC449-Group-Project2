# Lines 1 - .. will be borrowed from ProfAvery's hug/api
import configparser
import logging.config
import hug
import sqlite_utils
import datetime


# Load configuration
config = configparser.ConfigParser()
config.read("./etc/timeline.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# arguments to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Route
@hug.get("/timelines/")
def timelines(db: sqlite):
    return {"timelines": db["timelines"].rows}
