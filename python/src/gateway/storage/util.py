import pika, json


def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)  # returns an id
    except:
        return "server error", 500

    message = {
        "video_id": str(file_id),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
        )
    except:
        pass
