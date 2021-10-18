# Lines 1 - 22 will be borrowed from Professor Avery's hug/api
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

@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_user(
        response,
        id: hug.types.number,
        username: hug.types.text,
        bio: hug.types.text,
        email: hug.types.text,
        password: hug.types.text,
        db: sqlite,
):
    users = db["users"]

    user = {
        "id": id,
        "username": username,
        "bio": bio,
        "email": email,
        "password": password,
        "db": db,
    }

    try:
        users.insert(user)
        user["id"] = users.last_pk
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    response.set_header("Location", f"/users/{user['id']}")
    return user

@hug.get("/users/{id}")
def retrieve_book(response, id: hug.types.number, db: sqlite):
    users = []
    try:
        user = db["users"].get(id)
        users.append(user)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"users": user}

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
