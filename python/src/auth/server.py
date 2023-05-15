import jwt, os
from datetime import datetime, timedelta
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["SQL_HOST"] = os.environ.get("SQL_HOST")
server.config["SQL_USER"] = os.environ.get("SQL_USER")
server.config["SQL_PW"] = os.environ.get("SQL_PW")
server.config["SQL_DB"] = os.environ.get("SQL_DB")
server.config["SQL_PORT"] = os.environ.get("SQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization  # for jwt,username,password -> authentication stuff
    if not auth:
        return "missing credentials", 401

    cursor = mysql.connection.cursor()
    # A cursor keeps track of the position in the result set, and allows you to perform multiple operations row by row against a result set, with or without returning to the original table.
    res = cursor.execute(
        "SELECT email, password FROM user WHERE email=%s",
        (auth.username,),  # passing the params as a tuple
    )

    # res is array of rows
    if res > 0:
        row = cursor.fetchone()
        print(res, row)
        # cursor.fetchone method retrieves the next row of a query result set and returns a single sequence, or None if no more rows are available.
        # row is a tuple
        email = row[0]
        password = row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    jwt_token = request.headers["Authorization"]

    if not jwt_token:
        return "missing credentials", 401

    jwt_token = jwt_token.split(" ")[1]  # Format: Bearer token

    try:
        decoded = jwt.decode(
            jwt_token, os.environ.get("JWT_SECRET")
        )  # will throw exception if the token cannot be decoded/ is modified
    except:
        return "You're not authorized", 401

    return decoded, 200


def createJWT(username, secret, isAdmin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.utcnow() + timedelta(days=1),  # expiration
            "iat": datetime.utcnow(),  # issued at
            "admin": isAdmin,
        },
        secret,
        # algorithm="HS256",  # Which is the default
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", debug=True)
