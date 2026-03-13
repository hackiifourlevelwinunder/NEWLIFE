from flask import Flask, jsonify, render_template
import hashlib
import time
from datetime import datetime, timedelta

app = Flask(__name__)

ROUND_TIME = 60
PREVIEW_TIME = 40

SERVER_SEED = "ankush_rng_secret"


def get_reset_time():

    now = datetime.now()

    reset = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if now < reset:
        reset -= timedelta(days=1)

    return reset


def get_round():

    reset = get_reset_time()

    now = datetime.now()

    diff = now - reset

    seconds = int(diff.total_seconds())

    return seconds // 60 + 1


def get_period():

    date = datetime.now().strftime("%Y%m%d")

    round_number = get_round()

    return f"{date}10001{round_number:04d}"


def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


def generate_number(period):

    data = f"{SERVER_SEED}-{period}"

    h = hashlib.sha256(data.encode()).hexdigest()

    return int(h, 16) % 10


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()

    time_left = get_time_left()

    number = generate_number(period)

    if time_left > PREVIEW_TIME:
        number = None

    return jsonify({
        "period": period,
        "time_left": time_left,
        "number": number
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
