from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS
import string
import random

app = Flask(__name__)

REDIS_URL = "redis://:password@localhost:6379/0"

redis_client = FlaskRedis(app)

from app import redis_client

CORS(app)

@app.route("/url/add", methods=["POST"])
def add_url():
    url = request.json.get("url")
    key = "".join([random.SystemRandom().choice(string.ascii_letters) for i in range(20)])

    redis_client.set(key, url)
    return jsonify(key)


@app.route("/url/get", methods=["GET"])
def get_urls():
    # all_keys = redis_client.keys('*http://localhost:3000*')
    all_keys = list(redis_client.scan_iter("*"))
    values = [redis_client.get(key) for key in all_keys]
    return jsonify([{ "link": all_keys[i].decode("utf-8"), "url":values[i].decode("utf-8")} for i in range(len(values))])


@app.route("/url/get-value", methods=["POST"])
def get_url():
    link = request.json.get("link")
    url = redis_client.get(link)

    return jsonify(url)


if __name__ == "__main__":
    app.run(debug=True)