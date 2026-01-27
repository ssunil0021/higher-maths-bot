from flask import Flask, request
import os, redis, json

app = Flask(__name__)

r = redis.from_url(os.getenv("REDIS_URL"))

@app.route("/")
def home():
    return "Webhook running"

@app.route("/webhook", methods=["POST"])
def webhook():
    r.lpush("updates", request.data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
