from flask import Flask
from redis import Redis, RedisError

import os
import socket

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>could not connect to Redis. Connection is disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
        "<b>Hostname:</b> {hostname} <br />" \
        "<b>visits:</b> {visits}"

    return html.format(name=os.getenv("NAME", "world"), hostname = socket.gethostname(), visits=visits)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "80"))
    app.run(host="0.0.0.0", port=port)