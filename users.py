# Lines 1 - 22 will be borrowed from Professor Avery's hug/api, the rest follow the example
# in of that same api.py
import configparser
import logging.config
import hug
import sqlite_utils

# Load Configuration
config = configparser.ConfigParser()
config.read("./etc/users.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguments to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Route
@hug.get("/users/")
def books(db: sqlite):
    return {"users": db["users"].rows}

# Create a user
@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_user(
        response,
        # id: hug.types.number,
        username: hug.types.text,
        bio: hug.types.text,
        email: hug.types.text,
        password: hug.types.text,
        db: sqlite,
):
    users = db["users"]
    # the following line replaces %20 with spaces for the database
    # this may need to be done to other columns of the database, but for now, just bio
    bio = bio.replace("%20", " ")
    user = {
        "username": username,
        "bio": bio,
        "email": email,
        "password": password,
    }

    try:
        users.insert(user)
        user["id"] = users.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['id']}")
    return user

# Search for a user
@hug.get(
    "/search",
    example=[
        "username=user_name",
        "email=emailaddress@mail.com",
    ],
)
def search(request, db: sqlite, logger: log):
    users = db["users"]

    conditions = []
    values = []

    if "published" in request.params:
        conditions.append("username = ?")
        values.append(request.params["username"])

    for column in ["username", "bio", "email"]:
        if column in request.params:
            conditions.append(f"{column} LIKE ?")
            values.append(f"%{request.params[column]}%")

        if conditions:
            where = " AND ".join(conditions)
            logger.debug('WHERE "%s", %r', where, values)
            return {"users": users.rows_where(where, values)}
        else:
            return {"users": users.rows}

# authenticate
@hug.get("/authenticate/",
         example=[
             "username=user_name",
             "password=password"
         ],
)
def authenticateUser(request, db: sqlite, logger: log):

    username = request.params.get("username")
    password = request.params.get("password")

    # the following code was modeled after
    # https://stackabuse.com/a-sqlite-tutorial-with-python/
    # specific section: "Querying the Database"
    # and https://sqlite-utils.datasette.io/en/stable/python-api.html
    #
    for row in db.query('SELECT password FROM users WHERE username = ?', [username]):
        if row['password'] == password:
            print("lol")
            return {"statusCode": 200,"message": "Successfully Authenticated!" }
        else:
            request.status = hug.falcon.HTTP_404
        return {"error": str(request.status), "message": "Invalid Username or Password"}

#
# Access Followers
#
@hug.get("/followers/")
def followers(db: sqlite):
    return {"followers": db["followers"].rows}

#
# add follower
#
@hug.post("/followers/", status=hug.falcon.HTTP_201)
def addFollower(
        response,
        follower_id: hug.types.number,
        following_id: hug.types.number,
        db: sqlite,
):
    followers = db["followers"]

    follow = {
        "follower_id": follower_id,
        "following_id": following_id,
    }

    try:
        followers.insert(follow)
        follow["id"] = followers.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{follow['id']}")
    return follow