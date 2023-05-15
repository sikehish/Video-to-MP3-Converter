import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFs(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

channel = connection.channel()


@server.route("/login", method=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access)  # deserializing jwt payload
    if access["admin"]:
        if len(request.files) > 1 or not len(
            request.files
        ):  # exactly 1 file should be uploaded
            return "exactly 1 file required", 400

        for file in request.files.values():
            err = util.upload(file, fs, channel, access)
            if err:
                return err

        return "success!", 200
    else:
        return "not authroized!", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
