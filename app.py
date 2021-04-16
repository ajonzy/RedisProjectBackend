from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_heroku import Heroku

import random
import string

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"

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