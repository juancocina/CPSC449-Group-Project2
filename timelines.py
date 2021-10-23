# Lines 1 - .. will be borrowed from ProfAvery's hug/api
import configparser
import logging.config
import hug
import sqlite_utils
from datetime import datetime
import requests

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

#
# authentication
# ... was not fully implemented before deadline ...
@hug.get("/authentication/",
         example=[
             "username=user_name",
             "password=password"
         ],
)
def callAuthentication(request):
    username = request.params.get("username")
    password = request.params.get("password")

    authenticated = requests.get(f'http://localhost:8001/authenticate/?username={username}&password={password}')
    result = authenticated.json()
    if result["statusCode"] == 200:
        return result
    else:
        return False


# Gets public timeline
@hug.get("/timelines/")
def timelines(db: sqlite):
    return {"timelines": db["timelines"].rows_where(order_by="timestamp desc")}

# Posts onto the timeline
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

# user timeline
"""
@hug.get("/timelimes/{id}")
def getUserTimeline(response, username: hug.types.text, db:sqlite):
    tweets = []
    try:
        tweet = db["timelines"].get(username)
        tweets.append(tweet)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"timelines": tweet}
"""

# search for user tweets/posts/messages (userTimeline)
@hug.get(
    "/timelines/",
    example=[
        "username=user_name"
        "text=text"
    ],
)
def getUserTimeline(request, db: sqlite, logger:log):
    tweets = db["timelines"]

    conditions = []
    values = []

    if "published" in request.params:
        conditions.append("username = ?")
        values.append(request.params["username"])

    for column in ["username", "text"]:
        if column in request.params:
            conditions.append(f"{column} LIKE ?")
            values.append(f"%{request.params[column]}%")

        if conditions:
            where = " AND ".join(conditions)
            logger.debug('WHERE "%s", %r', where, values)
            return {"timelines": tweets.rows_where(where, values)}
        else:
            return {"timelines": tweets.rows_where(order_by="timestamp desc")}

#
# Home timeline (retrieves posts from users you follow)
#


#
# Repost
#