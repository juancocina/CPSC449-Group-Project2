# Lines 1 - .. will be borrowed from ProfAvery's hug/api
import configparser
import logging.config
import hug
import sqlite_utils
from datetime import datetime

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

@hug.post("/timelines/", status=hug.falcon.HTTP_201)
def postTweet(
        response,
        username: hug.types.text,
        text: hug.types.text,
        db: sqlite,
):
    timelines = db["timelines"]

    timestamp = datetime.utcnow()
    text = text.replace("%20", " ")
    tweet = {
        "username": username,
        "text": text,
        "timestamp": timestamp,
    }

    try:
        timelines.insert(tweet)
        tweet["id"] = timelines.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"err": str(e)}

    response.set_header("Location", f"/timelines/{tweet['id']}")
    return tweet

