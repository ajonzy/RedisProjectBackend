from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_heroku import Heroku

import random
import string

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://:p575d3c88a43bc080d6163c0852f694e439760ddf38555f6d30ccb64b9fe671a5@ec2-3-210-18-223.compute-1.amazonaws.com:21699"

CORS(app)
heroku = Heroku(app)

redis_client = FlaskRedis(app)


@app.route("/url/set", methods=["POST"])
def set_url():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON.")

    url = request.json.get("url")

    key = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(20)])

    redis_client.set(key, url)
    return jsonify(key)

@app.route("/url/get", methods=["GET"])
def get_all_keys():
    all_keys = redis_client.keys("*")
    return jsonify([key.decode("utf-8") for key in all_keys])

@app.route("/url/get/<key>", methods=["GET"])
def get_key(key):
    return jsonify(redis_client.get(key).decode("utf-8"))


if __name__ == "__main__":
    app.run(debug=True)